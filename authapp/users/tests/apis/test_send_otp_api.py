import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def otp_url():
    return reverse("api:users:send_otp")


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


class TestSendOtpApiView:
    def test_send_otp_success(self, api_client, otp_url):
        response = api_client.post(otp_url, data={"phone": "09123456789"})
        assert response.status_code == status.HTTP_200_OK
        assert "otp_code" in response.data

    def test_send_otp_invalid_phone_length(self, api_client, otp_url):
        response = api_client.post(otp_url, data={"phone": "12345"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_send_otp_with_throttling(self, api_client, otp_url):
        phone_number = "09123456789"

        for _ in range(3):
            response = api_client.post(otp_url, data={"phone": phone_number})
            assert response.status_code == status.HTTP_200_OK

        response = api_client.post(otp_url, data={"phone": phone_number})
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    def test_send_otp_invalid_phone_characters(self, api_client, otp_url):
        response = api_client.post(otp_url, data={"phone": "invalid_num"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
