from rest_framework_simplejwt.views import TokenObtainPairView

from authapp.users.throttles import LoginThrottle


class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginThrottle]
