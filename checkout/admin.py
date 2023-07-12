
from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'merchant', 'customer_name', 'customer_email', 'customer_phone_no', 'shipping_address',
                    'created_at', 'payment_currency', 'total_amount', 'payment_status']
    readonly_fields = ['id', 'merchant', 'customer_name', 'customer_email', 'customer_phone_no', 'shipping_address', 'products']
