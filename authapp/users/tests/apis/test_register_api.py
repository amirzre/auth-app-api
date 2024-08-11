import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authapp.users.models import BaseUser, UserProfile
from authapp.utils.otp import store_otp


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def register_url():
    return reverse("api:users:register")


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def existing_user(db):
    return BaseUser.objects.create_user(phone="09123456789", password="Test@1234")


@pytest.mark.django_db
class TestRegisterApiView:
    def test_register_user_success(self, api_client, register_url):
        phone_number = "09876543210"
        otp_code = "123456"

        store_otp(phone=phone_number, otp_code=otp_code, ttl=120)

        data = {
            "phone": phone_number,
            "password": "Strong@1234",
            "otp_code": otp_code,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
        }

        response = api_client.post(register_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert BaseUser.objects.filter(phone=phone_number).exists()

    def test_register_user_invalid_otp(self, api_client, register_url):
        data = {
            "phone": "09876543210",
            "password": "Strong@1234",
            "otp_code": "invalid",
            "first_name": "user",
            "last_name": "test",
            "email": "user.test@example.com",
        }

        response = api_client.post(register_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_existing_phone(self, api_client, register_url, existing_user):
        data = {
            "phone": existing_user.phone,
            "password": "Strong@1234",
            "otp_code": "123456",
            "first_name": "user",
            "last_name": "test",
            "email": "new.email@example.com",
        }

        response = api_client.post(register_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_existing_email(self, api_client, register_url, existing_user):
        UserProfile.objects.create(
            user=existing_user, first_name="user", last_name="test", email="user.test@example.com"
        )

        data = {
            "phone": "09876543210",
            "password": "Strong@1234",
            "otp_code": "123456",
            "first_name": "user",
            "last_name": "test",
            "email": "user.test@example.com",
        }

        response = api_client.post(register_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already exists." in str(response.data)

    def test_register_user_throttle_limit(self, api_client, register_url):
        phone_number = "09876543210"

        data = {
            "phone": phone_number,
            "password": "Strong@1234",
            "otp_code": "123456",
            "first_name": "user",
            "last_name": "test",
            "email": "user.test@example.com",
        }

        for _ in range(3):
            response = api_client.post(register_url, data=data)
            assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client.post(register_url, data=data)
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
