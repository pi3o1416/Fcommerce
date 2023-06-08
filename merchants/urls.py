
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MerchantModelViewSet


merchant_router = DefaultRouter()
merchant_router.register('', MerchantModelViewSet)

app_name = 'merchant'
urlpatterns = [
    path('', include(merchant_router.urls))
]
