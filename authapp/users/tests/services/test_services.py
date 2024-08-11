from unittest.mock import patch

import pytest

from authapp.core.exceptions import ApplicationError
from authapp.users.models import BaseUser, UserProfile
from authapp.users.services import create_profile, create_user, register_user, send_otp_code
from authapp.utils.otp import generate_otp, store_otp


@pytest.mark.django_db
class TestServices:
    def test_create_user(self):
        phone = "09123456789"
        password = "test@123"
        user = create_user(phone=phone, password=password)
        assert BaseUser.objects.get(phone=phone) == user
        assert user.check_password(password)

    def test_create_profile(self):
        user = BaseUser.objects.create_user(phone="09123456789", password="test@123")
        profile = create_profile(user=user, first_name="John", last_name="Doe", email="john.doe@example.com")
        assert UserProfile.objects.get(user=user) == profile
        assert profile.first_name == "John"
        assert profile.last_name == "Doe"
        assert profile.email == "john.doe@example.com"

    def test_register_user_valid_otp(self):
        phone = "09123456789"
        password = "test@123"
        first_name = "John"
        last_name = "Doe"
        email = "john.doe@example.com"

        otp_code = generate_otp()
        store_otp(phone=phone, otp_code=otp_code, ttl=120)

        user = register_user(
            phone=phone, first_name=first_name, last_name=last_name, email=email, otp_code=otp_code, password=password
        )
        assert BaseUser.objects.get(phone=phone) == user
        assert UserProfile.objects.get(user=user).first_name == first_name

    def test_register_user_invalid_otp(self):
        with pytest.raises(ApplicationError, match="Invalid phone or expired OTP code."):
            register_user(
                phone="09123456789",
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                otp_code="invalid_otp",
            )

    def test_register_user_already_registered(self):
        phone = "09123456789"
        otp_code = generate_otp()
        store_otp(phone=phone, otp_code=otp_code, ttl=120)

        create_user(phone=phone, password="test@123")

        with pytest.raises(ApplicationError, match="User already registered."):
            register_user(
                phone=phone, first_name="John", last_name="Doe", email="john.doe@example.com", otp_code=otp_code
            )

    def test_register_user_without_password(self):
        phone = "09123456789"
        otp_code = generate_otp()
        store_otp(phone=phone, otp_code=otp_code, ttl=120)

        user = register_user(
            phone=phone, first_name="John", last_name="Doe", email="john.doe@example.com", otp_code=otp_code
        )
        assert BaseUser.objects.get(phone=phone) == user

    @patch("authapp.users.services.store_otp")
    @patch("authapp.users.services.generate_otp")
    @patch("authapp.users.services.logger")
    def test_send_otp_code(self, mock_logger, mock_generate_otp, mock_store_otp):
        phone = "091361112233"

        otp_code = "268675"
        mock_generate_otp.return_value = otp_code
        mock_store_otp.return_value = True  

        returned_otp_code = send_otp_code(phone=phone)

        mock_store_otp.assert_called_once_with(phone=phone, otp_code=otp_code, ttl=120)

        assert returned_otp_code == otp_code

        mock_logger.info.assert_called_once_with(f"OTP code for {phone} is {otp_code}.")
