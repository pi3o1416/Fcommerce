
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..models import Merchant


class PasswordValidationMixin(serializers.Serializer):
    def validate_password(self, password):
        validate_password(password=password)
        return password

    def validate_retype_password(self, retype_password):
        password = self.initial_data.get('password')
        if password is not None and password != retype_password:
            raise ValidationError("Password and Retype password should be same")
        return retype_password


class MerchantCreateSerializer(PasswordValidationMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    retype_password = serializers.CharField(write_only=True)

    class Meta:
        model = Merchant
        fields = ['id', 'name', 'merchant_id', 'password', 'retype_password', 'is_published', 'integrate_facebook']
        read_only_fields = ['id']
        extra_kwargs = {
            'is_published': {'read_only': True},
            'integrate_facebook': {'read_only': True}
        }

    def validate(self, attrs):
        attrs.pop('retype_password')
        return super().validate(attrs=attrs)


class MerchantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id', 'name', 'is_published']
        read_only_fields = ['id']


class MerchantPasswordChangeSerializer(PasswordValidationMixin, serializers.ModelSerializer):
    current_password = serializers.CharField()
    password = serializers.CharField()
    retype_password = serializers.CharField()

    class Meta:
        model = Merchant
        fields = ['current_password', 'password', 'retype_password']

    def validate_current_password(self, current_password):
        if self.instance is not None and self.instance.check_password(current_password) is True:
            return current_password
        raise ValidationError("Invalid Current Password")


class MerchantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id', 'name', 'merchant_id', 'is_published', 'integrate_facebook', 'created_at']
        read_only_fields = ['id', 'name', 'merchant_id', 'is_published', 'integrate_facebook', 'created_at']
