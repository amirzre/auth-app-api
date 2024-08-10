import logging

from django.core.exceptions import ValidationError

from authapp.users.models import BaseUser, UserProfile
from authapp.utils.otp import generate_otp, store_otp, validate_otp

logger = logging.getLogger(__name__)


def register_user(
    *,
    phone: str,
    first_name: str,
    last_name: str,
    email: str,
    otp_code: str,
    password=None,
) -> BaseUser:
    if not validate_otp(phone=phone, entered_otp=otp_code):
        raise ValidationError("Invalid or expired OTP code.")

    if BaseUser.objects.filter(phone=phone).exists():
        raise ValidationError("User already registered.")

    user = BaseUser.objects.create_user(phone=phone, password=password)

    UserProfile.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    user.phone_verified = True
    user.save()

    return user


def send_otp_code(*, phone: str) -> str:
    """
    Generate and send OTP code.
    """
    otp_code = generate_otp()

    store_otp(phone=phone, otp_code=otp_code, ttl=120)

    # Simulate sending the OTP via SMS
    # print(f"OTP code for {phone} is {otp_code}.")
    logger.info(f"OTP code for {phone} is {otp_code}.")

    return otp_code
