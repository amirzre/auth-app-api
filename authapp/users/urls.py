from django.urls import path

from .apis import SendOtpApiView

urlpatterns = [path("send-otp/", SendOtpApiView.as_view(), name="send_otp")]
