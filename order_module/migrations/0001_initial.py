# Generated by Django 4.2 on 2023-04-21 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import order_module.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_module', '0001_initial'),
        ('product_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(verbose_name='نهایی شده/نشده')),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='تاریخ پرداخت')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_module.productcoupon', verbose_name='تخفیف')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبدهای خرید کاربران',
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='نام گیرنده')),
                ('last_name', models.CharField(max_length=255, verbose_name='نام خانوادگی گیرنده')),
                ('national_code', models.CharField(max_length=255, validators=[order_module.validators.is_valid_iran_code], verbose_name='کد ملی گیرنده')),
                ('phone_number', models.CharField(max_length=255, validators=[order_module.validators.is_valid_phone_number], verbose_name='شماره تماس گیرنده')),
                ('house_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='پلاک خونه')),
                ('building_unit', models.CharField(blank=True, max_length=255, null=True, verbose_name='واحد خونه')),
                ('postal_code', models.CharField(max_length=255, validators=[order_module.validators.is_valid_postal_code], verbose_name='کد پستی')),
                ('address', models.TextField(verbose_name='آدرس پستی')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_module.city', verbose_name='شهر مقصد')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_module.province', verbose_name='استان مقصد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'مشخصات تحویل گیرنده',
                'verbose_name_plural': 'مشخصات تحویل گیرندگان',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.IntegerField(blank=True, null=True, verbose_name='قیمت نهایی تکی محصول')),
                ('count', models.IntegerField(validators=[order_module.validators.min_count_validator], verbose_name='تعداد')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_module.order', verbose_name='سبد خرید')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'جزییات سبد خرید',
                'verbose_name_plural': 'لیست جزییات سبدهای خرید',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='shipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_module.shipment', verbose_name='اطلاعات تحویل'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
