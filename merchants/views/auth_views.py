
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from services.utils import customize_response
from services.constants import ErrorTypes
from ..serializers import MyTokenRefreshSerializer


def _set_cookie(response=None, cookie_name=None, cookie_value=None, max_age=3600 * 24 * 15):
    """
    Set httponly cookie in response.
    Get response, cookie_name, cookie value as parameter
    retrun response.
    """
    assert response is not None, 'Response should not be null'
    assert cookie_name is not None, 'Cookie Name should not be null'
    assert cookie_value is not None, 'Cookie Value should not be null'
    response.set_cookie(cookie_name, cookie_value, max_age,
                        httponly=True, samesite="None", secure=True)
    return response


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            refresh_token = response.data.get('refresh')
            response = _set_cookie(
                response=response,
                cookie_name='refresh_token',
                cookie_value=refresh_token
            )
            del response.data['refresh']
        # Formatting Error message with desired response form
        if response.status_code >= 400:
            response.data['message'] = 'Incorrect merchant name or password'
            response.data['error_type'] = ErrorTypes.INVALID_CREDENTIAL.value
        else:
            response = customize_response(response=response, custom_message='Login Successful')
        return super().finalize_response(request, response, *args, **kwargs)


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
    permission_classes = [AllowAny]

    def finalize_response(self, request, response, *args, **kwargs):
        try:
            refresh_token = response.data['refresh']
            response = _set_cookie(
                response=response,
                cookie_name='refresh_token',
                cookie_value=refresh_token
            )
            del response.data['refresh']
            response = customize_response(response=response, custom_message='Generate access token from refresh token')
        except Exception as exception:
            response.data['message'] = 'Failed to retrieve access token from refresh token'
            if isinstance(exception, KeyError):
                response.data['error_type'] = ErrorTypes.INVALID_REFRESH_TOKEN.value
        finally:
            return super().finalize_response(request, response, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logout view. Remove refresh token from cookie
        """
        response = Response({'detail': ['Logout Successful']}, status=status.HTTP_200_OK)
        refresh_token = RefreshToken(request.COOKIES.get('refresh_token'))
        refresh_token.blacklist()
        response.delete_cookie("refresh_token")
        if 'refresh_token' in request.COOKIES:
            del request.COOKIES['refresh_token']
        return customize_response(response=response, custom_message='Logout Successful')
