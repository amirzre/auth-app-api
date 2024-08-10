from django.urls import path

from .apis import LoginApiView, RegisterApiView, SendOtpApiView

urlpatterns = [
    path("login/", LoginApiView.as_view(), name="login"),
    path("register/", RegisterApiView.as_view(), name="register"),
    path("send-otp/", SendOtpApiView.as_view(), name="send_otp"),
]
