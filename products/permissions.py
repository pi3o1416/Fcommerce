
from rest_framework.permissions import BasePermission
from .models import MerchantProduct


class IsProductOwner(BasePermission):
    def has_object_permission(self, request, view, merchant_product: MerchantProduct):
        product_owner_id = merchant_product.merchant_id
        if product_owner_id == request.user.id:
            return True
        return False
