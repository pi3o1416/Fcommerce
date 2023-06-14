
from django.urls import path, include
from .views import MerchantModelViewSet, MyTokenObtainPairView, MyTokenRefreshView, LogoutView
from .routers import CustomRouter


router = CustomRouter(trailing_slash=True)
router.register('', MerchantModelViewSet)

app_name = 'merchant'
urlpatterns = [
    path('auth/login/', MyTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh-token/', MyTokenRefreshView.as_view(), name='refresh-token'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
