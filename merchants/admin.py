
from django.contrib import admin
from .models import Merchant


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Merchant._meta.fields]
