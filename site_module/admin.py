from django.contrib import admin

# Register your models here.
from site_module.models import SiteSetting, SiteEmailBanner, Province, City


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteEmailBanner)
class SiteEmailBannerAdmin(admin.ModelAdmin):
    pass


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass
