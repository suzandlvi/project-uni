from django.contrib import admin

# Register your models here.
from order_module.models import Order, OrderDetail, Shipment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    pass


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    pass
