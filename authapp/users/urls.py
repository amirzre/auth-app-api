from django.urls import path

from .apis import RegisterApiView, SendOtpApiView

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
    path("send-otp/", SendOtpApiView.as_view(), name="send_otp"),
]
