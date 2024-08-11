from unittest.mock import patch

import pytest
from django.core.cache import cache

from authapp.utils.otp import generate_otp, get_otp, store_otp, validate_otp


@pytest.mark.django_db
class TestOTP:
    def test_generate_otp(self):
        otp = generate_otp()
        assert len(otp) == 6
        assert otp.isdigit()

    def test_store_otp(self):
        phone = "1234567890"
        otp = "654321"
        store_otp(phone, otp, ttl=300)
        cache_key = f"otp:{phone}"
        stored_otp = cache.get(cache_key)
        assert stored_otp == otp

    def test_get_otp(self):
        phone = "1234567890"
        otp = "654321"
        cache_key = f"otp:{phone}"
        cache.set(cache_key, otp, timeout=300)
        retrieved_otp = get_otp(phone)
        assert retrieved_otp == otp

    def test_validate_otp_success(self):
        phone = "1234567890"
        otp = "654321"
        store_otp(phone, otp, ttl=300)
        assert validate_otp(phone, otp) is True
        assert cache.get(f"otp:{phone}") is None

    def test_validate_otp_failure(self):
        phone = "1234567890"
        otp = "654321"
        wrong_otp = "123456"
        store_otp(phone, otp, ttl=300)
        assert validate_otp(phone, wrong_otp) is False
        assert cache.get(f"otp:{phone}") == otp

    @patch("django.core.cache.cache.get")
    def test_otp_expires(self, mock_cache_get):
        phone = "1234567890"
        mock_cache_get.return_value = None
        assert validate_otp(phone, "654321") is False
