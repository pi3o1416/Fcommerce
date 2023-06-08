
from django.db import connections
from django.http import Http404
from django.core.exceptions import PermissionDenied

from rest_framework import exceptions
from rest_framework.response import Response


def set_rollback():
    for db in connections.all():
        if db.settings_dict['ATOMIC_REQUESTS'] and db.in_atomic_block:
            db.set_rollback(True)


def exception_handler(exc: Exception, context=None, message=None, error_type=None):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        data = {
            'detail': exc.detail,
            'error_type': error_type,
            'message': message
        }
        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None


def customize_response(response, custom_message):
    if response.data is None:
        response.data = {
            'detail': 'Successful'
        }
    else:
        response.data = {
            'detail': response.data
        }
    response.data['message'] = custom_message
    return response
