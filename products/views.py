
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from services.paginations import CustomPageNumberPagination
from services.utils import customize_response, exception_handler
from services.constants import ErrorTypes
from .permissions import IsProductOwner
from .models import Product
from .serializers import ProductSerializer


class MerchantProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
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

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
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

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return customize_response(response=response, custom_message='Merchant Product Delete Successful')
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Product Delete Failed',
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action in ['retrieve', 'update', 'destroy']:
            permissions += [IsProductOwner]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        return ProductSerializer

    def get_queryset(self):
        if self.action == 'list':
            merchant_products = Product.objects.merchant_products(merchant=self.request.user)
            return merchant_products.filter_from_query_params(request=self.request)
        return Product.objects.all()

    def get_serializer_context(self):
        if self.action == 'create':
            return {
                'request': self.request
            }
        else:
            return super().get_serializer_context()
