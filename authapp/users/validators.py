import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def phone_validator(phone: str):
    """
    Validate phone number.
    """
    regex = re.compile(r"^09\d{9}$")
    if regex.search(phone) is None:
        raise ValidationError(_("Invalid phone number."), code="invalid_phone_number")


def number_validator(password: str):
    regex = re.compile("[0-9]")
    if regex.search(password) is None:
        raise ValidationError(_("Password must include number."), code="password_must_include_number")


def letter_validator(password: str):
    regex = re.compile("[a-zA-Z]")
    if regex.search(password) is None:
        raise ValidationError(_("Password must include letter."), code="password_must_include_letter")


def special_char_validator(password: str):
    regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    if regex.search(password) is None:
        raise ValidationError(_("Password must include special char."), code="password_must_include_special_char")


def email_validator(email: str):
    regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if regex.search(email) is None:
        raise ValidationError(_("Email is invalid."), code="email_invalid")
