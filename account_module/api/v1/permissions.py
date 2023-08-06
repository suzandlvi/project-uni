from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    def has_permission(self, request, view):
        # if not request.user.is_verified:
        #     return False
        return True
