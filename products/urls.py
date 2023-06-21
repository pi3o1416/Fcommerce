
from django.urls import path, include

from .views import MerchantProductsViewSet
from .routers import MerchantProductRouter


router = MerchantProductRouter(trailing_slash=True)
router.register('merchant-products', MerchantProductsViewSet)

app_name = 'products'
urlpatterns = [
    path('', include(router.urls))
]
