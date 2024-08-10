import random

from django.core.cache import cache


def generate_otp() -> str:
    """
    Generate random OTP code.
    """
    return str(random.randint(100000, 999999))


def store_otp(phone: str, otp_code: str, ttl=300) -> None:
    """
    Store OTP code in Redis with a time-to-live (TTL).
    """
    cache_key = f"otp:{phone}"
    cache.set(cache_key, otp_code, timeout=ttl)


def get_otp(phone: str) -> str:
    """
    Retrieve OTP code from Redis.
    """
    cache_key = f"otp:{phone}"
    return cache.get(cache_key)


def validate_otp(phone: str, entered_otp: str) -> bool:
    """
    Check if the entered OTP matches the one in Redis.
    """
    stored_otp = get_otp(phone)
    if stored_otp and stored_otp == entered_otp:
        cache.delete(f"otp:{phone}")
        return True
    return False
