from django.http import HttpRequest
from rest_framework.permissions import BasePermission, SAFE_METHODS


class OrderPermission(BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj):
        return False
        # print(obj)
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return obj.user.id == request.user.id

    # def has_permission(self, request: HttpRequest, view):
    #     if request.user.is_superuser:
    #         return True
    #     else:
    #         return request.method in SAFE_METHODS
