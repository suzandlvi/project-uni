from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def valid_pct(value):
    if value.endswith("%"):
        return float(value[:-1]) / 100
    else:
        try:
            return float(value)
        except ValueError:
            raise ValidationError(
                _('%(value)s is not a valid pct'),
                params={'value': value},
            )


def coupon_code_validator(value):
    if len(value) < 4:
        raise ValidationError('کد نمیواند کمتر از 4 کارکتر باشد')
    return value
