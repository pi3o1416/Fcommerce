
from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from services.constants import ErrorTypes
from services.paginations import CustomPageNumberPagination
from services.utils import exception_handler, customize_response
from ..exceptions import MerchantDeleteException
from ..models import Merchant
from ..filters import MerchantFilter
from ..serializers import MerchantCreateSerializer, MerchantDetailSerializer, MerchantUpdateSerializer, MerchantPasswordChangeSerializer


class MerchantModelViewSet(ModelViewSet):
    model = Merchant
    lookup_field = 'id'
    queryset = Merchant.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MerchantFilter
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
        except MerchantDeleteException as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Account Delete Failed',
                error_type=ErrorTypes.DB_RESTRICTED.value
            )

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return customize_response(response, 'Merchant Update Successful')
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message='Merchant Account Update Failed',
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action == ['create', 'list', 'retrieve', 'update', 'destroy']:
            permissions += [IsAdminUser]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action == 'create':
            return MerchantCreateSerializer
        elif self.action == 'update':
            return MerchantUpdateSerializer
        return MerchantDetailSerializer


class AuthMerchantViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Merchant.objects.all()

    @action(methods=['get'], detail=False, url_path='detail')
    def auth_merchant_detail(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=request.user)
        return Response(
            data={
                'detail': serializer.data,
                'message': 'Account Detail Retrieved'
            }
        )

    @action(methods=['put'], detail=False, url_path='update')
    def auth_merchant_update(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    'detail': serializer.data,
                    'message': 'Account Update Successful'
                }
            )
        return Response(
            data={
                'detail': serializer.errors,
                'message': 'Account Update Failed'
            }
        )

    @action(methods=['post'], detail=False, url_path='change-password')
    def auth_merchant_change_password(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    'message': 'Password Change Successful'
                }
            )
        return Response(
            data={
                'detail': serializer.errors,
                'message': 'Password Change Failed'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def get_serializer_class(self):
        if self.action == 'auth_merchant_update':
            return MerchantUpdateSerializer
        elif self.action == 'auth_merchant_change_password':
            return MerchantPasswordChangeSerializer
        return MerchantDetailSerializer
