import re

from django.core.exceptions import ValidationError


def check_name(value: str):
    for el in value:
        if not el.isalpha() and not el.isspace():
            raise ValidationError("Name can only contain letters and spaces")


def check_phone_number(value):
    if not re.match(r'^\+359\d{9}$', value):
        raise ValidationError("Phone number must start with a '+359' followed by 9 digits")
