
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import MerchantProductsViewSet


router = SimpleRouter(trailing_slash=True)
router.register('merchant-products', MerchantProductsViewSet)

app_name = 'products'
urlpatterns = [
    path('', include(router.urls))
]
