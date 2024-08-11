import re

from django.utils.translation import gettext_lazy as _

from authapp.core.exceptions import ApplicationError


def phone_validator(phone: str):
    """
    Validate phone number.
    """
    regex = re.compile(r"^09\d{9}$")
    if regex.search(phone) is None:
        raise ApplicationError(message=_("Invalid phone number."))


def number_validator(password: str):
    regex = re.compile("[0-9]")
    if regex.search(password) is None:
        raise ApplicationError(message=_("Password must include number."))


def letter_validator(password: str):
    regex = re.compile("[a-zA-Z]")
    if regex.search(password) is None:
        raise ApplicationError(message=_("Password must include letter."))


def special_char_validator(password: str):
    regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    if regex.search(password) is None:
        raise ApplicationError(message=_("Password must include special char."))


def email_validator(email: str):
    regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if regex.search(email) is None:
        raise ApplicationError(message=_("Email is invalid."))
