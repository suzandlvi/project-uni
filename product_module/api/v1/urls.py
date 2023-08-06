from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "product_module_api"
router = DefaultRouter()
router.register("products", views.ProductAPIView, basename="product")
router.register("product-categories", views.ProductCategoryAPIView, basename="product_category")
router.register("product-brands", views.ProductBrandAPIView, basename="product_brand")

urlpatterns = [
    path("", include(router.urls)),
]
