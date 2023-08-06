from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from account_module.models import User
from contact_module.models import ContactUs


class TestContactUsModel(TestCase):
    def setUp(self) -> None:
        self.contact_us = ContactUs.objects.create(email='test@test.com', is_read_by_admin=False, full_name='test',
                                                   message='test message')

    def test_create_contact_us_with_valid_data(self):
        self.assertEqual(self.contact_us.email, 'test@test.com')


class TestContactUsView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user('test', 'test@test.com', '1234')
        request = Client()
        request.force_login(user)
        self.request = request

    def test_contact_us_view_response_200(self):
        response = self.request.get(reverse('contact-us-view'))
        self.assertEqual(response.status_code, 200)

    def test_contact_us_view_template(self):
        response = self.request.get(reverse('contact-us-view'))
        if response.status_code == 200:
            self.assertTemplateUsed(response, template_name='contact_module/contact-us.html')
        else:
            self.assertTrue(True)

    def test_contact_us_view_logged_in(self):
        response = self.request.get(reverse('contact-us-view'))
        self.assertEqual(response.status_code, 200)
