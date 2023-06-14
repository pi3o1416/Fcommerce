
from django.contrib import admin
from .models import Merchant


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'merchant_id', 'integrate_facebook', 'publish_shop', 'is_staff',
                    'is_superuser', 'is_active', 'created_at']

    def add_view(self, *args, **kwargs):
        self.exclude = ('integrate_facebook', 'publish_shop')
        return super(MerchantAdmin, self).add_view(*args, **kwargs)
