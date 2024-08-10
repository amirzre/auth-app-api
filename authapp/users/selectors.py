from authapp.users.models import BaseUser, UserProfile


def get_profile(user: BaseUser) -> UserProfile:
    return UserProfile.objects.get(user=user)
