
from django.urls import path, include
from .views import MerchantModelViewSet
from .routers import CustomRouter


router = CustomRouter(trailing_slash=True)
router.register('', MerchantModelViewSet)

app_name = 'merchant'
urlpatterns = [
    path('', include(router.urls))
]
