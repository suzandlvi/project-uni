from django.test import TestCase

# Create your tests here.
from unittest import TestCase

from account_module.forms import LoginForm


class TestForm(TestCase):
    def test_login_form_valid_data(self):
        form = LoginForm(data={
            'email': 'amirhossein6168@GMAail.Com',
            'password': '1234'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_valid_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

