from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ContactUsView.as_view(), name='contact-us-view'),
    path('api/v1/', include('contact_module.api.v1.urls')),
]