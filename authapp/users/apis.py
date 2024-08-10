from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.users.services import send_otp_code
from authapp.users.validators import phone_validator


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
