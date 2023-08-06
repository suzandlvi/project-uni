from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "api-v1"
router = DefaultRouter()
router.register("contact-us", views.ContactUsAPIView, basename="contact_us")
urlpatterns = [
    path("", include(router.urls)),
]
