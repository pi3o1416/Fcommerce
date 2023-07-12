
from django.urls import path, include

from .views import MerchantProductsViewSet, CustomerMerchantProducts
from .routers import MerchantProductRouter


router = MerchantProductRouter(trailing_slash=True)
router.register('merchant-products', MerchantProductsViewSet)

app_name = 'products'
urlpatterns = [
    path('merchant-products-for-customer/<str:merchant_name>/', CustomerMerchantProducts.as_view(), name='customer-merchant-products'),
    path('', include(router.urls))
]
