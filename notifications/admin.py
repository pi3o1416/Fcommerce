
from django.contrib import admin
from .models import FacebookAPIErrorLog


@admin.register(FacebookAPIErrorLog)
class FacebookAPINotificationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FacebookAPIErrorLog._meta.fields]
    readonly_fields = [field.name for field in FacebookAPIErrorLog._meta.fields]
