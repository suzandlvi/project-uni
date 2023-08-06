from django.http import HttpRequest
from rest_framework.permissions import BasePermission, SAFE_METHODS

from contact_module.api.v1.serializers import ContactUsSerializer


class IsAdminOrCreateOnly(BasePermission):
    # def has_object_permission(self, request: HttpRequest, view, obj):
    #     if request.method in SAFE_METHODS:
    #         return True
    #     else:
    #         return obj.author.user.id == request.user.id

    def has_permission(self, request: HttpRequest, view):
        if request.user.is_superuser:
            return True
        else:
            return request.method == "POST"
