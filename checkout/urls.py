
from django.urls import path
from .views import PlaceOrder, OrderList


urlpatterns = [
    path('place-order/', PlaceOrder.as_view(), name='place-order'),
    path('order-list/', OrderList.as_view(), name='order-list'),
]
