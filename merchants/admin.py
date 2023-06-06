
from django.contrib import admin
from .models import Merchant


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Merchant._meta.fields]

    def add_view(self, *args, **kwargs):
        self.exclude = ('integrate_facebook', 'publish_shop')
        return super(MerchantAdmin, self).add_view(*args, **kwargs)
