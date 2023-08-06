import re

from django.core.exceptions import ValidationError


def min_count_validator(value):
    if value < 1:
        raise ValidationError("تعداد نمیتواند کمتر از 1 باشد")
    else:
        return value


def is_valid_iran_code(value):
    if not re.search(r'^\d{10}$', value): return False
    check = int(value[9])
    s = sum(int(value[x]) * (10 - x) for x in range(9)) % 11
    return check == s if s < 2 else check + s == 11


def is_valid_phone_number(value):
    res = re.search("^(0|0098|\+98)9(0[1-5]|[1 3]\d|2[0-2]|98)\d{7}$", value)
    if bool(res):
        return True
    else:
        return False


def contains_number(value):
    for character in value:
        if not character.isdigit():
            return False
    return True


def is_valid_postal_code(value):
    res = re.search("\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b", value)
    if bool(res):
        return True
    else:
        return False
