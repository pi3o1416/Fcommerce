
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from services.paginations import CustomPageNumberPagination
from services.utils import customize_response, exception_handler
from services.constants import ErrorTypes
from .permissions import IsProductOwner
from .models import MerchantProduct
from .serializers import MerchantProductSerializer
from .tasks import add_product_on_facebook, delete_product, sync_inventory_with_facebook, update_product_on_facebook


class MerchantProductsViewSet(ModelViewSet):
    queryset = MerchantProduct.objects.all()
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return customize_response(response=response, custom_message='Merchant Product Create Successful')
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Product Create Failed',
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )

    def perform_create(self, serializer):
        # Create Product on facebook inventory
        product = serializer.save()
        add_product_on_facebook.delay(product_id=product.id)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return customize_response(response=response, custom_message='Merchant Product list')

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request=request, *args, **kwargs)
            return customize_response(response=response, custom_message='Merchant Product Retrieve Successful')
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Product Not Found',
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def update(self, request, id, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            # Update on facebook inventory
            return customize_response(response=response, custom_message='Merchant Product Update Successful')
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Product Update Failed',
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Product Update Failed',
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )

    def perform_update(self, serializer):
        product = serializer.save()
        update_product_on_facebook.delay(product_id=product.id)

    def destroy(self, request, id, *args, **kwargs):
        try:
            # Delete from facebook inventory
            response = super().destroy(request, *args, **kwargs)
            return customize_response(response=response, custom_message='Merchant Product Delete Successful')
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Product Delete Failed',
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def perform_destroy(self, instance: MerchantProduct):
        delete_product.delay(product_id=instance.id)

    @action(methods=['get'], detail=False, url_path='sync-with-facebook')
    def sync_inventory_with_facebook(self, request):
        merchant = request.user
        sync_inventory_with_facebook.delay(merchant_id=merchant.id)
        response = Response(data={'detail': 'Request Accepted'}, status=status.HTTP_202_ACCEPTED)
        return customize_response(response, 'A Sync process is in Progress')

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action in ['retrieve', 'update', 'destroy']:
            permissions += [IsProductOwner]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        return MerchantProductSerializer

    def get_queryset(self):
        if self.action == 'list':
            merchant_products = MerchantProduct.objects.merchant_products(merchant=self.request.user)
            return merchant_products.filter_from_query_params(request=self.request)
        return MerchantProduct.objects.all()

    def get_serializer_context(self):
        if self.action == 'create':
            return {
                'request': self.request
            }
        else:
            return super().get_serializer_context()
