from django.urls import path, include
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart_view'),
    path('add-to-order/', views.add_product_to_order, name='add_product_to_order_view'),
    path('shipment/', views.ShipmentView.as_view(), name='shipment_view'),
    path('api/v1/', include("order_module.api.v1.urls")),
]
