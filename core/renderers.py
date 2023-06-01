from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        custom_data = {
            'status': None,
            'data': None,
            'error': None,
        }
        error_message = {
            'message': None,
            'type': None,
            'detail': None,
        }
        response = renderer_context.get("response")
        custom_data["status"] = response.status_code
        if response.status_code >= 400:
            error_message['detail'] = data['detail']
            error_message['type'] = data['type']
            error_message['message'] = data['message']
            custom_data['error'] = error_message
        else:
            custom_data['data'] = data
        return super().render(custom_data, accepted_media_type, renderer_context)
