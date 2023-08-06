from django import forms

from contact_module.models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(
                attrs={'id': 'contact-name', 'class': 'form-control', 'placeholder': 'نام و نام خانوادگی ...'}),
            'email': forms.EmailInput(
                attrs={'id': 'contact-email', 'class': 'form-control', 'placeholder': 'email ...'}),
            'message': forms.Textarea(attrs={'id': 'contact-text', 'class': 'form-control', 'cols': 30, 'rows': 3,
                                             'placeholder': 'متن پیام ...'}),
        }
        labels = {
            'full_name': 'نام و نام خانوادگی خود را وارد کنید',
            'email': 'ایمیل خود را وارد کنید',
            'message': 'متن پیام را وارد کنید',
        }
