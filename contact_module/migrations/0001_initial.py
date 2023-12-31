# Generated by Django 4.2 on 2023-04-21 09:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=300, validators=[django.core.validators.EmailValidator()], verbose_name='ایمیل')),
                ('full_name', models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')),
                ('message', models.TextField(verbose_name='متن تماس با ما')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('is_read_by_admin', models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')),
            ],
            options={
                'verbose_name': 'تماس با ما',
                'verbose_name_plural': 'لیست تماس با ما',
            },
        ),
        migrations.CreateModel(
            name='ContactUsResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان پاسخ')),
                ('message', models.TextField(verbose_name='متن پاسخ')),
                ('is_answered', models.BooleanField(default=True, verbose_name='پاسخ داده شده')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_us_response', to='contact_module.contactus', verbose_name='مربوط به پیام')),
            ],
            options={
                'verbose_name': 'پاسخ پیام',
                'verbose_name_plural': 'پاسخ های پیام',
            },
        ),
    ]
