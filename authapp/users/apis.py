from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.api.mixins import ApiAuthMixin
from authapp.users.models import BaseUser, UserProfile
from authapp.users.selectors import get_profile
from authapp.users.services import register_user, send_otp_code
from authapp.users.validators import (
    email_validator,
    letter_validator,
    number_validator,
    phone_validator,
    special_char_validator,
)


class SendOtpApiView(APIView):
    class InputOtpSerializer(serializers.Serializer):
        phone = serializers.CharField(
            required=True,
            validators=[
                MinLengthValidator(limit_value=11),
                phone_validator,
            ],
        )

    class OutputOtpSerializer(serializers.Serializer):
        otp_code = serializers.CharField()

    @extend_schema(request=InputOtpSerializer, responses=OutputOtpSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.InputOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            otp_code = send_otp_code(phone=serializer.validated_data.get("phone"))
        except ValidationError:
            return Response(
                data={{"error": serializer.errors}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        output_serializer = self.OutputOtpSerializer({"otp_code": otp_code})
        return Response(data=output_serializer.data, status=status.HTTP_200_OK)


class RegisterApiView(APIView):
    class InputRegistrSerializer(serializers.Serializer):
        phone = serializers.CharField(
            required=True,
            validators=[
                MinLengthValidator(limit_value=11),
                phone_validator,
            ],
        )
        password = serializers.CharField(
            required=True,
            validators=[
                MinLengthValidator(limit_value=8),
                number_validator,
                letter_validator,
                special_char_validator,
            ],
        )
        otp_code = serializers.CharField(required=True, validators=[MinLengthValidator(limit_value=6)])
        first_name = serializers.CharField(required=True, max_length=50)
        last_name = serializers.CharField(required=True, max_length=50)
        email = serializers.EmailField(required=True, validators=[email_validator])

        def validate_phone(self, phone):
            if BaseUser.objects.filter(phone=phone).exists():
                raise serializers.ValidationError("Phone number already exists.")
            return phone

        def validate_email(self, email):
            if UserProfile.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already exists.")
            return email

    class OutputRegistrSerializer(serializers.ModelSerializer):
        first_name = serializers.CharField(source="profile.first_name")
        last_name = serializers.CharField(source="profile.last_name")
        email = serializers.EmailField(source="profile.email")

        class Meta:
            model = BaseUser
            fields = ("phone", "first_name", "last_name", "email")

    @extend_schema(request=InputRegistrSerializer, responses=OutputRegistrSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.InputRegistrSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = register_user(
                phone=serializer.validated_data.get("phone"),
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                email=serializer.validated_data.get("email"),
                otp_code=serializer.validated_data.get("otp_code"),
                password=serializer.validated_data.get("password"),
            )
        except ValidationError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

        output_serializer = self.OutputRegistrSerializer(user)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class ProfileApiView(ApiAuthMixin, APIView):
    class OutputProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserProfile
            fields = ("first_name", "last_name", "email")

    @extend_schema(responses=OutputProfileSerializer)
    def get(self, request, *args, **kwargs):
        profile = get_profile(user=request.user)
        return Response(
            self.OutputProfileSerializer(profile, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )
