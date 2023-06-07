
def handle_exception(exception, custom_message, error_type):
    exception.detail = {
        'message': custom_message,
        'detail': exception.detail,
        'error_type': error_type.value
    }
    raise exception


def customize_response(response, custom_message):
    response.data = {
        'message': custom_message,
        'detail': response.data
    }
    return response
