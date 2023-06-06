from django.apps import AppConfig


class MerchantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'merchants'

    def ready(self):
        try:
            from . import signals as _
        except Exception:
            pass
