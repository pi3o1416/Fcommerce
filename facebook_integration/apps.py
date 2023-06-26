from django.apps import AppConfig


class FacebookIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'facebook_integration'

    def ready(self):
        try:
            from . import signals as _
        except Exception:
            pass
