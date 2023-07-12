
from django.db import transaction
from django_countries.serializers import CountryFieldMixin
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import MerchantProduct


class MerchantProductSerializer(CountryFieldMixin, serializers.ModelSerializer):
    retailer_id = serializers.CharField(required=False)
    gtin = serializers.CharField(required=False)

    class Meta:
        model = MerchantProduct
        fields = [field.name for field in MerchantProduct._meta.fields if field.name not in ['facebook_id']]
        read_only_fields = ['merchant']

    def validate_retailer_id(self, value):
        if self.instance is not None and self.instance.retailer_id != value:
            raise ValidationError("Retailer ID is uneditable")
        if self.instance is None and MerchantProduct.objects.filter(retailer_id=value).exists():
            raise ValidationError("Retailer ID already exist")
        return value

    @transaction.atomic
    def create(self, validated_data: dict):
        """
        Create a new product. use the new product to create a merchant product
        and return MerchantProducts instance
        """
        merchant = self.context['request'].user
        merchant_product = MerchantProduct.objects.create(**validated_data, merchant=merchant)
        return merchant_product


class MerchantProductMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantProduct
        fields = ['name', 'url', 'image_url', 'currency', 'price', 'retailer_id', 'gtin']
