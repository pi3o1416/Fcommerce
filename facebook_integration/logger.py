
import json
import logging
from django.conf import settings


class FacebookAPIErrorLogger(logging.Logger):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.propagate = False

        # Retrieve the loggers and handlers configured in Django settings
        configured_loggers = settings.LOGGING.get('loggers', {})
        handlers = settings.LOGGING.get('handlers', {})

        # Configure the logger with the handlers from Django settings
        if self.name in configured_loggers:
            logger_settings = configured_loggers[self.name]
            logger_handlers = logger_settings.get('handlers', [])

            # Attach the specified handlers to the logger
            for handler_name in logger_handlers:
                if handler_name in handlers:
                    handler = logging._handlers[handler_name]
                    self.addHandler(handler)

    def error(self, message, merchant_id, response=None, *args, **kwargs):
        log_data = {
            "message": message,
            "response": response.json() if response is not None else None,
            "status_code": response.status_code if response is not None else None,
            "merchant_id": merchant_id
        }
        new_message = json.dumps(log_data)
        super().error(new_message, *args, **kwargs)


class FacebookAPIErrorHandler(logging.Handler):
    def emit(self, record):
        from notifications.models import FacebookAPIErrorLog
        log_message = json.loads(self.format(record))
        FacebookAPIErrorLog.objects.create(
            merchant_id=log_message['merchant_id'],
            api_response_status_code=log_message['status_code'],
            api_response=log_message['response'],
            message=log_message['message']
        )
