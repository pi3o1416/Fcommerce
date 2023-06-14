from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import serializers


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        raise InvalidToken("No valid Token found in cookie 'refresh_token'")


class AccessTokenSerializer(serializers.Serializer):
    """
    Only for documentations
    """
    access = serializers.CharField()
