
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, merchant):
        if request.user.is_authenticated is True and request.user.id == merchant.id:
            return True
        return False
