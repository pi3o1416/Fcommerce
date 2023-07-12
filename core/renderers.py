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
            custom_data['message'] = data['message'] if 'message' in data else ''
            custom_data['error'] = data['detail'] if 'detail' in data else data
            custom_data['error-type'] = data['error_type'] if 'error_type' in data else ''
        else:
            custom_data['message'] = data['message'] if 'message' in data else ''
            custom_data['data'] = data['detail'] if 'detail' in data else data
        return super().render(custom_data, accepted_media_type, renderer_context)
