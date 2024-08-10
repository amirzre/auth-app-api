import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def phone_validator(phone: str):
    """
    Validate phone number.
    """
    regex = re.compile("/^((98|\+98|0098|0)*(9)[0-9]{9})+$/")
    if regex.search(phone) is None:
        raise ValidationError(_("Invalid phone number."), code="invalid_phone_number")
