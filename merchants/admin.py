
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Merchant


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'merchant_id', 'signature_key', 'integrate_facebook', 'is_published', 'is_staff',
                    'is_superuser', 'is_active', 'created_at']

    fieldsets = (
        (_("Merchant info"), {"fields": ("name", "merchant_id", "signature_key", "password")}),
        (_("Shop Management"), {"fields": ("is_published", "integrate_facebook")}),
        (_("Important dates"), {"fields": ("last_login",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None,
            {
                "classes": ("wide",),
                "fields": ("name", "merchant_id", "signature_key", "password"),
            },
         ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
