import pytest
from django.core.exceptions import ObjectDoesNotExist

from authapp.users.models import BaseUser, UserProfile
from authapp.users.selectors import get_profile


@pytest.mark.django_db
class TestSelectors:
    def test_get_profile_valid_user(self):
        user = BaseUser.objects.create_user(phone="09123456789", password="test@123")
        profile = UserProfile.objects.create(
            user=user, first_name="user", last_name="test", email="user.test@example.com"
        )

        retrieved_profile = get_profile(user=user)

        assert retrieved_profile == profile
        assert retrieved_profile.first_name == "user"
        assert retrieved_profile.last_name == "test"
        assert retrieved_profile.email == "user.test@example.com"

    def test_get_profile_user_without_profile(self):
        user = BaseUser.objects.create_user(phone="09123456789", password="test@123")

        with pytest.raises(ObjectDoesNotExist):
            get_profile(user=user)

    def test_get_profile_multiple_users(self):
        user1 = BaseUser.objects.create_user(phone="09123456787", password="test@123")
        profile1 = UserProfile.objects.create(
            user=user1, first_name="user1", last_name="test", email="user1@example.com"
        )

        user2 = BaseUser.objects.create_user(phone="09123456780", password="test@123")
        profile2 = UserProfile.objects.create(
            user=user2, first_name="user2", last_name="test", email="user2@example.com"
        )

        retrieved_profile1 = get_profile(user=user1)
        retrieved_profile2 = get_profile(user=user2)

        assert retrieved_profile1 == profile1
        assert retrieved_profile2 == profile2
        assert retrieved_profile1.first_name == "user1"
        assert retrieved_profile2.first_name == "user2"
