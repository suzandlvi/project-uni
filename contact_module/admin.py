from django.contrib import admin

# Register your models here.
from contact_module.models import ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'created_date', 'is_read_by_admin']
