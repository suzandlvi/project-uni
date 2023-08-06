from django import forms
import re

from order_module.models import Shipment
from order_module.validators import is_valid_iran_code, is_valid_phone_number, is_valid_postal_code


class ShipmentForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    national_code = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    province = forms.CharField(required=True)
    city = forms.CharField(required=True)
    house_number = forms.CharField(required=False)
    building_unit = forms.CharField(required=False)
    postal_code = forms.CharField(required=True)
    address = forms.CharField(required=True)

    def clean_national_code(self):
        value = self.cleaned_data['national_code']
        res = is_valid_iran_code(value)
        if res:
            return value
        else:
            raise forms.ValidationError("کد ملی وارد شده صحیح نمیباشد")

    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        res = is_valid_phone_number(value)
        if res:
            return value
        else:
            raise forms.ValidationError("شماره موبایل وارد شده صحیح نمیباشد")

    def clean_postal_code(self):
        value = self.cleaned_data['postal_code']
        # res = is_valid_postal_code(value)
        # if res:
        #     return value
        # else:
        #     raise forms.ValidationError("کد پستی وارد شده معتبر نمیباشد")
        return value
