from django import forms

from account_module.models import User
from utils.normalize_email import normalize_email


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput({'class': 'form-control', 'placeholder': 'نام ...'}),
            'last_name': forms.TextInput({'class': 'form-control', 'placeholder': 'نام خانوادگی ...'}),
            'email': forms.EmailInput({'class': 'form-control', 'placeholder': 'email...'}),
            'password': forms.PasswordInput({'class': 'form-control', 'id': 'password', 'placeholder': 'رمز عبور ...'})
        }
        labels = {
            'first_name': 'نام خود را وارد کنید',
            'last_name': 'نام خانوادگی خود را وارد کنید',
            'email': 'ایمیل خود را وارد کنید',
            'password': 'رمز عبور خود را وارد کنید',
        }

    def save(self, commit=True):
        m = super(RegisterForm, self).save(commit=False)
        m.email = normalize_email(m.email)
        if commit:
            m.save()
        return m


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput({'class': 'form-control', 'placeholder': 'email...'}),
                             label='ایمیل خود را وارد کنید', required=True)
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput({'class': 'form-control', 'id': 'password', 'placeholder': 'رمز عبور ...'}),
        label='رمز عبور خود را وارد کنید')


class EditUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'نام ...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'نام خانوادگی ...'}),
            'avatar': forms.FileInput(
                attrs={'class': 'form-control-file mb-3 btn btn-info', 'accept': 'image/png, image/gif, image/jpeg'}),
            # 'address': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': '5', 'placeholder': 'آدرس ...'})
        }
        labels = {
            'first_name': 'نام خود را وارد کنید',
            'last_name': 'نام خانوادگی خود را وارد کنید',
            'avatar': 'تصویر آواتار خود را انتخاب کنید',
            # 'address': 'آدرس خود را وارد کنید',
        }


class EditUserPasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور فعلی")
    new_password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور جدید")

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        if current_password == new_password:
            raise forms.ValidationError('رمز عبور فعلی با رمز عبور جدید نمیتواند یکی باشد')

    # def clean_new_password(self):
    #     return password_strength_check(self.cleaned_data.get('new_password'))
