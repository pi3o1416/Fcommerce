
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import FacebookIntegrationData


class FacebookIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookIntegrationData
        fields = ['id', 'access_token', 'business_id', 'catalog_id', 'page_id', 'page_data']

    def create(self, validated_data: dict):
        merchant = self.context['request'].user
        integration_data = FacebookIntegrationData.objects.create(
            merchant=merchant,
            **validated_data
        )
        return integration_data

    def validate(self, attrs):
        merchant = self.context['request'].user
        if merchant.integrate_facebook is False:
            return attrs
        raise ValidationError('Facebook Integration allready completed')


class FacebookIntegrationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookIntegrationData
        fields = ['id', 'access_token', 'business_id', 'catalog_id', 'page_id', 'page_data']


class FacebookIntegrationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookIntegrationData
        fields = ['id', 'merchant', 'access_token', 'catalog_id', 'page_id', 'page_data']

    def to_representation(self, instance: FacebookIntegrationData):
        return instance.decrypted_data()
