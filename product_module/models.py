from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

from product_module.validators import coupon_code_validator, valid_pct
from utils.unique_slug_generator import unique_slug_generator


class ProductCategory(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(
        max_length=300,
        db_index=True,
        verbose_name='عنوان'
    )
    slug = models.SlugField(
        default='',
        blank=True,
        null=True,
        db_index=True,
        allow_unicode=True,
        unique=True,
        verbose_name='عنوان در url'
    )
    is_active = models.BooleanField(
        verbose_name='فعال / غیرفعال'
    )
    is_delete = models.BooleanField(
        verbose_name='حذف شده / نشده'
    )

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = unique_slug_generator(self)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        unique_together = ('slug', 'parent',)


class ProductBrand(models.Model):
    title = models.CharField(
        max_length=300,
        verbose_name='نام برند',
        db_index=True
    )
    english_title = models.CharField(
        default='',
        blank=True,
        null=True,
        unique=True,
        max_length=300,
        verbose_name='نام در url',
        db_index=True
    )
    is_active = models.BooleanField(
        verbose_name='فعال / غیرفعال'
    )

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(
        max_length=300,
        verbose_name='نام محصول'
    )
    category = models.ForeignKey(
        'ProductCategory',
        on_delete=models.SET_NULL,
        null=True,
        related_name='product_categories',
        verbose_name='دسته بندی ها'
    )
    image = models.ImageField(
        upload_to='images/products',
        verbose_name='تصویر محصول'
    )
    brand = models.ForeignKey(
        'ProductBrand',
        on_delete=models.CASCADE,
        related_name='product_brands',
        verbose_name='برند'
    )
    price = models.IntegerField(
        verbose_name='قیمت'
    )
    # size = models.CharField(
    #     max_length=50,
    #     verbose_name='ابعاد'
    # )
    # weight = models.FloatField(
    #     verbose_name='وزن'
    # )
    # screen_size = models.CharField(
    #     max_length=50,
    #     verbose_name='سایز صفحه نمایش'
    # )
    # cpu = models.CharField(
    #     max_length=50,
    #     verbose_name='پردازنده'
    # )
    # gpu = models.CharField(
    #     max_length=50,
    #     verbose_name='پردازنده گرافیکی'
    # )
    # camera_resolution = models.IntegerField(
    #     verbose_name='رزولوشن دوربین'
    # )
    # software = models.CharField(
    #     max_length=50,
    #     verbose_name='سیستم عامل'
    # )
    # battery = models.CharField(
    #     max_length=50,
    #     verbose_name='باطری'
    # )
    # release_date = models.CharField(
    #     max_length=50,
    #     verbose_name='تاریخ عرضه'
    # )
    quantity = models.IntegerField(default=1, verbose_name='موجودی')
    description = models.TextField(
        verbose_name='توضیحات اصلی',
        db_index=True,
    )
    slug = models.SlugField(
        default="",
        blank=True,
        null=True,
        db_index=True,
        max_length=200,
        unique=True,
        allow_unicode=True,
        verbose_name='عنوان در url'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='فعال / غیرفعال'
    )
    is_delete = models.BooleanField(
        verbose_name='حذف شده / نشده',
        default=False
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ قرار گیری محصول',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     print(self.id)
    #     if not self.slug:
    #         self.slug = unique_slug_generator(self)
    #         print(self.slug)
    #     return super().save(*args, **kwargs)

    def vote_avg(self):
        if self.productvote_set.first():
            return round(self.productvote_set.aggregate(vote_avg=Avg('vote')).get('vote_avg'))
        return 0

    def get_absolute_url(self):
        return reverse('product_detail_view', kwargs={'slug': self.slug})


class ProductDetail(models.Model):
    category = models.ForeignKey("ProductCategory", on_delete=models.CASCADE, verbose_name="دسته بندی مربوطه")
    key = models.CharField(max_length=255, db_index=True, verbose_name="مقدار کلید")

    class Meta:
        verbose_name = "جزییات محصول"
        verbose_name_plural = "جزییات محصولات"
        # indexes = ["key"]

    def __str__(self):
        return f"{self.category.title} => {self.key}"


class ProductDetailValue(models.Model):
    product_detail = models.ForeignKey("ProductDetail", on_delete=models.CASCADE,
                                       related_name="product_detail_attributes", verbose_name="جزییات مربوطه")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_attributes",
                                verbose_name="محصول مربوطه")
    value = models.CharField(max_length=255, db_index=True, verbose_name="مقدار")

    class Meta:
        verbose_name = "مقدار جزییات محصول"
        verbose_name_plural = "مقدار جزییات محصولات"
        # indexes = ["value"]
        ordering = ["product_detail__key"]

    def __str__(self):
        return f"{self.product_detail} => {self.value}"


class ProductVisit(models.Model):
    product = models.ForeignKey(
        'Product',
        related_name='product_visit',
        on_delete=models.CASCADE,
        verbose_name='محصول'
    )
    ip = models.CharField(
        max_length=30,
        verbose_name='آی پی کاربر'
    )
    user = models.ForeignKey(
        'account_module.User',
        verbose_name='کاربر',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(
        'Product',
        related_name='product_gallery',
        on_delete=models.CASCADE,
        verbose_name='محصول',
    )
    image = models.ImageField(
        upload_to='images/product-gallery',
        verbose_name='تصویر'
    )

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductComment(models.Model):
    COMMEND_MODES = {
        ('Good', 'خوب'),
        ('Bad', 'بد'),
        ('Poker', 'پوکر'),
    }
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='برای محصول')
    user = models.ForeignKey('account_module.User', on_delete=models.CASCADE, verbose_name='کاربر')
    commend_text = models.TextField(verbose_name='متن کامنت')
    commend_mode = models.CharField(choices=COMMEND_MODES, max_length=50, verbose_name='مود کامنت')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    is_accepted = models.BooleanField(verbose_name='تایید شده توسط ادمین', default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class ProductVote(models.Model):
    user = models.ForeignKey(
        to='account_module.User',
        verbose_name='کاربر رای دهنده',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to='Product',
        verbose_name='مربوط به محصول',
        on_delete=models.CASCADE
    )
    vote = models.IntegerField(
        verbose_name='امتیاز',
        db_index=True,
        validators=[
            MaxValueValidator(5, 'نمیتوانید بیشتر از 5 امتیاز برای محصول ثبت کنید'),
            MinValueValidator(1, 'نمیتوانید کمتر از 1 امتیاز برای محصول ثبت کنید'),
        ]
    )

    class Meta:
        verbose_name = 'امتیاز محصول'
        verbose_name_plural = 'امتیازات محصول'

    def __str__(self):
        return self.user.email


class ProductCoupon(models.Model):
    DISCOUNT_TYPES = {
        ('Percent', 'درصدی'),
        ('Price', 'قیمتی'),
    }
    coupon_code = models.CharField(max_length=10, db_index=True, validators=[coupon_code_validator],
                                   verbose_name='کد کوپن')
    discount_percent = models.CharField(blank=True, null=True, max_length=4, validators=[valid_pct],
                                        help_text='حتما از علامت (٪) در اخر استفاده کنید', verbose_name='درصد تخفیف')
    discount_price = models.PositiveIntegerField(blank=True, null=True, verbose_name='مقدار قیمتی تخفیف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')
    expires_date = models.DateTimeField(verbose_name='تاریخ انقضا')
    discount_type = models.CharField(choices=DISCOUNT_TYPES, max_length=8, verbose_name='نوع کوپن')

    class Meta:
        verbose_name = 'کوپن تخفیف'
        verbose_name_plural = 'کوپن های تخفیف'

    def __str__(self):
        return self.coupon_code

    @property
    def get_discount_percent(self):
        return float(self.discount_percent.strip('%'))


class TestDownload(models.Model):
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/')


@receiver(post_save, sender=Product)
def save_profile(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()
    pass
