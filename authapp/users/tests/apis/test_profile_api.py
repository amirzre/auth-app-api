import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from authapp.users.models import BaseUser, UserProfile


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def profile_url():
    return reverse("api:users:profile")


@pytest.fixture
def user(db):
    user = BaseUser.objects.create_user(phone="09123456789", password="Test@1234")
    UserProfile.objects.create(user=user, first_name="user", last_name="test", email="user.test@example.com")
    return user


@pytest.fixture
def auth_headers(user):
    refresh = RefreshToken.for_user(user)
    return {
        "HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}",
    }


@pytest.mark.django_db
class TestProfileApiView:
    def test_get_profile_success(self, api_client, profile_url, auth_headers):
        response = api_client.get(profile_url, **auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "user"
        assert response.data["last_name"] == "test"
        assert response.data["email"] == "user.test@example.com"

    def test_get_profile_unauthenticated(self, api_client, profile_url):
        response = api_client.get(profile_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_profile_with_invalid_token(self, api_client, profile_url):
        invalid_headers = {
            "HTTP_AUTHORIZATION": "Bearer invalidtoken",
        }
        response = api_client.get(profile_url, **invalid_headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_profile_with_missing_token(self, api_client, profile_url):
        missing_token_headers = {
            "HTTP_AUTHORIZATION": "",
        }
        response = api_client.get(profile_url, **missing_token_headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
