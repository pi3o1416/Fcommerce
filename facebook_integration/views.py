
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from products.tasks import sync_inventory_with_facebook
from services.constants import ErrorTypes
from services.paginations import CustomPageNumberPagination
from services.utils import customize_response, exception_handler
from .models import FacebookIntegrationData
from .serializers import FacebookIntegrationDetailSerializer, FacebookIntegrationSerializer, FacebookIntegrationUpdateSerializer


class FacebookIntegrationModelViewSet(ModelViewSet):
    queryset = FacebookIntegrationData.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return customize_response(response, 'Facebook Integration Successful')
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message='Facebook Integration Failed',
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )

    def perform_create(self, serializer):
        super().perform_create(serializer=serializer)
        sync_inventory_with_facebook.delay(self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, id, *args, **kwargs)
            return customize_response(response, 'Facebook Integration Data Retrieve Successful')
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message='Facebook Integration Data Retrieve Failed',
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, id, *args, **kwargs)
            return customize_response(response, 'Facebook Integration Data Update Successful')
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message='Facebook Integration Data Update Failed',
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message='Facebook Integration Data Update Failed',
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, id, *args, **kwargs)
            return customize_response(response, 'Facebook Integration Data Delete Successful')
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message='Facebook Integration Data Delete Failed',
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def get_serializer_class(self):
        if self.action == 'create':
            return FacebookIntegrationSerializer
        elif self.action == 'retrieve':
            return FacebookIntegrationDetailSerializer
        elif self.action == 'update':
            return FacebookIntegrationUpdateSerializer
        else:
            return FacebookIntegrationSerializer

    def get_object(self):
        if self.action in ['retrieve', 'update', 'destroy']:
            try:
                merchant = self.request.user
                facebook_info = merchant.facebook_info
                return facebook_info
            except Exception:
                raise Http404
        return super().get_object()
