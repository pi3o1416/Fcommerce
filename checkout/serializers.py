
import requests
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import Order


Merchant = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    _merchant_id = None
    _currency = None

    class Meta:
        model = Order
        fields = ['id', 'merchant', 'customer_name', 'customer_email', 'customer_phone_no', 'shipping_address', 'products']
        read_only_fields = ['merchant']

    def validate_products(self, products):
        # Validate Can not place an order without any products
        if not len(products) > 0:
            raise ValidationError("At least one product is necessery to place an order")
        # Validate All products can have a unique merchant
        merchant_ids = {product.merchant_id for product in products}
        if len(merchant_ids) > 1:
            raise ValidationError("All the products should be from same merchant")
        # Validate All product currency should be equal
        product_currencies = {product.currency for product in products}
        if len(product_currencies) > 1:
            raise ValidationError("All the products currency should be equal")
        self._merchant_id = next(iter(merchant_ids))
        self._currency = next(iter(product_currencies))
        return products

    def create(self, validated_data):
        assert self._merchant_id is not None, "Merchant id not set in validation"
        products = validated_data.pop('products')
        order = Order.objects.create(
            merchant_id=self._merchant_id,
            payment_currency=self._currency,
            **validated_data
        )
        order.products.set(products)
        return order


class TransactionSerializer(serializers.Serializer):
    pg_txnid = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    mer_txnid = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    risk_title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    risk_level = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_email = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_add1 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_add2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_state = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_postcode = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_country = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cus_fax = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    ship_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    ship_add1 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    ship_add2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    ship_city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    ship_state = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    ship_postcode = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    ship_country = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    desc = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    merchant_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    store_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    amount = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    amount_bdt = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    pay_status = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status_title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cardnumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    approval_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    payment_processor = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bank_trxid = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    payment_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    error_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    error_title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bin_country = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bin_issuer = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bin_cardtype = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bin_cardcategory = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    date = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    date_processed = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    amount_currency = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    rec_amount = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    processing_ratio = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    processing_charge = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    ip = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    currency = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    currency_merchant = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    convertion_rate = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    opt_a = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    opt_b = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    opt_c = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    opt_d = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    verify_status = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    call_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    email_send = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    doc_recived = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    checkout_status = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate(self, attrs):
        try:
            transaction_data = self._retrieve_transaction_data(order=self.instance)
            if transaction_data is not None and attrs['status_code'] == transaction_data['status_code']:
                return attrs
            raise ValidationError("Transaction ID Verification Failed")
        except Order.DoesNotExist:
            raise ValidationError("Invalid Transaction ID")

    def _retrieve_transaction_data(self, order):
        merchant = order.merchant
        request_data = {
            "request_id": order.transaction_id,
            "store_id": merchant.merchant_id,
            "signature_key": merchant.signature_key,
            "type": "json"
        }
        response = requests.post(url=settings.TRXN_DETAIL_URL, params=request_data)
        if response.status_code == 200 and 'status_code' in response.json():
            return response.json()
        return None

    def save(self):
        if self.instance is not None:
            self.instance.payment_status = self.validated_data.get('status_code')
            self.instance.pg_transaction_id = self.validated_data.get('pg_txnid')
            self.instance.save()
        return self.instance
