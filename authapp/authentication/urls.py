from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .apis import CustomTokenObtainPairView

urlpatterns = [
    path(
        "jwt/",
        include(
            (
                [
                    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
                    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
                    path("verify/", TokenVerifyView.as_view(), name="verify"),
                ],
                "jwt",
            )
        ),
    ),
]
