
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Merchant


class MerchantCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    retype_password = serializers.CharField()

    class Meta:
        model = Merchant
        fields = ['id', 'name', 'merchant_id', 'password', 'retype_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'retype_password': {'write_only': True}
        }

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate(self, *args, **kwargs):
        password = self.initial_data['password']
        retype_password = self.initial_data['retype_password']
        if password != retype_password:
            raise ValidationError("Password and Retype password is not same")
        return super().validate(*args, **kwargs)


class MerchantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id', 'name', 'password', 'retype_password']


class MerchantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [field.name for field in Merchant._meta.fields]
