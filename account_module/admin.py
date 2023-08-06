from django.contrib import admin

# Register your models here.
from account_module.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass