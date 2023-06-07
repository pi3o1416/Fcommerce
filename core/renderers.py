from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        custom_data = {
            'message': None,
            'status': None,
            'data': None,
            'error': None,
            'error-type': None,
        }
        response = renderer_context.get("response")
        custom_data["status"] = response.status_code
        if response.status_code >= 400:
            custom_data['message'] = data['message']
            custom_data['error'] = data['detail']
            custom_data['error-type'] = data['error_type']
        else:
            custom_data['message'] = data['message']
            custom_data['data'] = data['detail']
        return super().render(custom_data, accepted_media_type, renderer_context)
