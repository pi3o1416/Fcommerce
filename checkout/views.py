
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from checkout.exceptions import FailedToInitiatePayment

from services.utils import customize_response
from services.paginations import CustomPageNumberPagination
from .serializers import OrderSerializer, TransactionSerializer
from .pgadapter import PGAdapter
from .models import Order


class PlaceOrder(APIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                order = serializer.save()
                pgadapter = PGAdapter(order=order)
                response_data = pgadapter.initiate_payment()
                response = Response(data=response_data, status=status.HTTP_201_CREATED)
                return customize_response(response, 'Payment Initiated Successful')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FailedToInitiatePayment as exception:
            return Response(data=exception.__str__(), status=status.HTTP_400_BAD_REQUEST)


class OrderList(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    queryset = Order.objects.all()

    def get_queryset(self):
        merchant = self.request.user
        return self.queryset.filter(merchant=merchant)


class PaymentNotificationAPI(APIView):
    serializer_class = TransactionSerializer
    queryset = Order.objects.all()

    def post(self, request):
        order = self.get_object()
        serializer = self.serializer_class(instance=order, data=request.data)
        serializer.is_valid(raise_exception=True)

    def get_object(self):
        transaction_id = self.request.data.get('mer_txnid')
        order = get_object_or_404(self.queryset, transaction_id=transaction_id)
        return order
