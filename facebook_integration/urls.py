
from django.urls import path, include
from .routers import FacebookIntegrationRouter
from .views import FacebookIntegrationModelViewSet

router = FacebookIntegrationRouter()
router.register('', FacebookIntegrationModelViewSet)

app_name = 'facebook_integration'
urlpatterns = [
    path('', include(router.urls))
]
