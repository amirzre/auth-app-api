from django.urls import path

from .apis import LoginApiView, ProfileApiView, RegisterApiView, SendOtpApiView

urlpatterns = [
    path("login/", LoginApiView.as_view(), name="login"),
    path("register/", RegisterApiView.as_view(), name="register"),
    path("send-otp/", SendOtpApiView.as_view(), name="send_otp"),
    path("profile/", ProfileApiView.as_view(), name="profile"),
]
