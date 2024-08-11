from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAuthAPI:
    @pytest.fixture
    def user_data(self):
        return {"phone": "09361234550", "password": "test@123"}

    @pytest.fixture
    def create_user(self, create_user, user_data):
        create_user(phone=user_data["phone"], password=user_data["password"])

    def test_successful_login(self, api_client, create_user, user_data):
        url = reverse("api:authentication:jwt:login")
        response = api_client.post(url, user_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_token_refresh(self, api_client, create_user, user_data):
        url = reverse("api:authentication:jwt:login")
        response = api_client.post(url, user_data)
        refresh_token = response.data["refresh"]

        refresh_url = reverse("api:authentication:jwt:refresh")
        response = api_client.post(refresh_url, {"refresh": refresh_token})

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_token_verify(self, api_client, create_user, user_data):
        url = reverse("api:authentication:jwt:login")
        response = api_client.post(url, user_data)
        access_token = response.data["access"]

        verify_url = reverse("api:authentication:jwt:verify")
        response = api_client.post(verify_url, {"token": access_token})
        assert response.status_code == status.HTTP_200_OK

    @patch("authapp.users.throttles.LoginThrottle.allow_request", return_value=True)
    def test_unsuccessful_login(self, mock_throttle, api_client, user_data):
        url = reverse("api:authentication:jwt:login")
        user_data["password"] = "wrongpassword"
        response = api_client.post(url, user_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("authapp.users.throttles.LoginThrottle.allow_request")
    @patch("authapp.users.throttles.LoginThrottle.get_cache_key")
    @patch("authapp.users.throttles.LoginThrottle.get_history", return_value=[0, 0])
    def test_ip_block_after_failed_attempts(
        self, mock_get_history, mock_cache_key, mock_allow_request, api_client, create_user, user_data
    ):
        url = reverse("api:authentication:jwt:login")

        mock_cache_key.return_value = "login_testuser_ip"

        def allow_request_side_effect(*args, **kwargs):
            if len(mock_get_history.return_value) < 3:
                return True
            return False

        mock_allow_request.side_effect = allow_request_side_effect

        user_data["password"] = "wrongpassword"

        for _ in range(3):
            response = api_client.post(url, user_data)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        mock_allow_request.side_effect = lambda *args, **kwargs: False

        response = api_client.post(url, user_data)
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

        new_user_data = user_data.copy()
        new_user_data["phone"] = "09361112233"

        response = api_client.post(url, new_user_data)
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
