
from django.db import transaction
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from .models import Product, MerchantProducts


class ProductSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [field.name for field in Product._meta.fields if field.name not in ['facebook_id']]

    @transaction.atomic
    def create(self, validated_data: dict):
        """
        Create a new product. use the new product to create a merchant product
        and return MerchantProducts instance
        """
        product = Product.objects.create(**validated_data)
        merchant = self.context['request'].user
        MerchantProducts.objects.create(
            merchant=merchant,
            product=product
        )
        return product


class MerchantProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantProducts
        fields = '__all__'
