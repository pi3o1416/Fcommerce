
from django.contrib import admin

from .models import FacebookIntegrationData


@admin.register(FacebookIntegrationData)
class FacebookIntegrationDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'merchant', 'access_token', 'catalog_id', 'page_id', 'page_data']
