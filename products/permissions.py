
from rest_framework.permissions import BasePermission
from .models import Product


class IsProductOwner(BasePermission):
    def has_object_permission(self, request, view, product: Product):
        product_owner_id = product.product_owner.merchant_id
        if product_owner_id == request.user.id:
            return True
        return False
