from rest_framework.exceptions import APIException
from rest_framework import status


class MerchantDeleteException(APIException):
    status_code = status.HTTP_409_CONFLICT
