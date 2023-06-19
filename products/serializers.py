
from rest_framework import serializers
from .models import Product, MerchantProducts


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [field.name for field in Product._meta.fields]


class MerchantProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Product
        field = [field.name for field in MerchantProducts._meta.fields]
