
from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser

from services.constants import ErrorTypes
from services.paginations import CustomPageNumberPagination
from services.utils import exception_handler, customize_response
from ..models import Merchant
from ..serializers import MerchantCreateSerializer, MerchantDetailSerializer


class MerchantModelViewSet(ModelViewSet):
    model = Merchant
    queryset = Merchant.objects.all()
    lookup_field = 'id'
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return customize_response(response, 'Merchant Create Successful')
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Account Create Failed',
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return customize_response(response, 'Merchant List')

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, id, *args, **kwargs)
            return customize_response(response, 'Merchant Retrieved')
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Account Not Found',
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def destroy(self, request, id, *args, **kwargs):
        try:
            response = super().destroy(request, id, *args, **kwargs)
            return customize_response(response, 'Merchant Deleted')
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Account Not Found',
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def get_serializer_class(self):
        if self.action == 'create':
            return MerchantCreateSerializer
        return MerchantDetailSerializer

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter_from_query_params(request=self.request)
        return self.queryset
