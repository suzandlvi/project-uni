from django.urls import path
from . import views

urlpatterns = [
    path("order/", views.OrderAPIView.as_view(), name="order-detail-api-view"),
    path("order-detail/", views.OrderDetailAPIView.as_view(), name="order-detail-api-view"),
    path("add-to-cart/", views.OrderAddAPIView.as_view(), name="order-add-api-view"),
    path("shipment/", views.ShipmentAPIView.as_view(), name="shipment-api-view"),
]