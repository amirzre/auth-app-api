import pytest

from authapp.core.exceptions import ApplicationError
from authapp.users.validators import (
    email_validator,
    letter_validator,
    number_validator,
    phone_validator,
    special_char_validator,
)


class TestValidators:
    def test_phone_validator_valid(self):
        phone = "09123456789"
        assert phone_validator(phone) is None

    def test_phone_validator_invalid(self):
        with pytest.raises(ApplicationError, match="Invalid phone number."):
            phone_validator("1234567890")
        with pytest.raises(ApplicationError, match="Invalid phone number."):
            phone_validator("08123456789")
        with pytest.raises(ApplicationError, match="Invalid phone number."):
            phone_validator("0912345678")
        with pytest.raises(ApplicationError, match="Invalid phone number."):
            phone_validator("091234567890")
        with pytest.raises(ApplicationError, match="Invalid phone number."):
            phone_validator("abcdefghijk")

    def test_number_validator_valid(self):
        assert number_validator("password1") is None
        assert number_validator("12345") is None

    def test_number_validator_invalid(self):
        with pytest.raises(ApplicationError, match="Password must include number."):
            number_validator("password")
        with pytest.raises(ApplicationError, match="Password must include number."):
            number_validator("")

    def test_letter_validator_valid(self):
        assert letter_validator("password") is None
        assert letter_validator("abc123") is None
        assert letter_validator("A1") is None

    def test_letter_validator_invalid(self):
        with pytest.raises(ApplicationError, match="Password must include letter."):
            letter_validator("123456")
        with pytest.raises(ApplicationError, match="Password must include letter."):
            letter_validator("")

    def test_special_char_validator_valid(self):
        assert special_char_validator("pass@word1") is None
        assert special_char_validator("1234@#$") is None

    def test_special_char_validator_invalid(self):
        with pytest.raises(ApplicationError, match="Password must include special char."):
            special_char_validator("password1")
        with pytest.raises(ApplicationError, match="Password must include special char."):
            special_char_validator("123456")
        with pytest.raises(ApplicationError, match="Password must include special char."):
            special_char_validator("")

    def test_email_validator_valid(self):
        assert email_validator("test@example.com") is None
        assert email_validator("user.name+tag+sorting@example.com") is None

    def test_email_validator_invalid(self):
        with pytest.raises(ApplicationError, match="Email is invalid."):
            email_validator("plainaddress")
        with pytest.raises(ApplicationError, match="Email is invalid."):
            email_validator("@missingusername.com")
        with pytest.raises(ApplicationError, match="Email is invalid."):
            email_validator("username@.com")
        with pytest.raises(ApplicationError, match="Email is invalid."):
            email_validator("username@com")
        with pytest.raises(ApplicationError, match="Email is invalid."):
            email_validator("username@domain..com")
