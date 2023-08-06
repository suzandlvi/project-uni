from django.core.validators import validate_email
from django.db import models


# Create your models here.
class ContactUs(models.Model):
    email = models.EmailField(max_length=300, validators=[validate_email], verbose_name='ایمیل')
    full_name = models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='متن تماس با ما')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.full_name



class ContactUsResponse(models.Model):
    contact = models.ForeignKey('ContactUs', on_delete=models.CASCADE, related_name='contact_us_response',
                                verbose_name='مربوط به پیام')
    title = models.CharField(max_length=50, verbose_name='عنوان پاسخ')
    message = models.TextField(verbose_name='متن پاسخ')
    is_answered = models.BooleanField(default=True, verbose_name='پاسخ داده شده')

    class Meta:
        verbose_name = 'پاسخ پیام'
        verbose_name_plural = 'پاسخ های پیام'

    def __str__(self):
        return self.contact.__str__()
