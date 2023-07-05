
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import MerchantProduct


@admin.register(MerchantProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MerchantProduct._meta.fields]
    fieldsets = (
        (_('Required Fields'), {'fields': ('merchant', 'name', 'description', 'url', 'image_url', 'currency', 'price')}),
        (_('Unique Identifier (It is recommanded NOT to manually change these values)'), {'fields': ('gtin', 'retailer_id')}),
        (_('Product'), {'fields': ('condition', 'availability', 'brand', 'category', 'color', 'expiration_date',
                                   'additional_image_urls', 'additional_variant_attributes', 'size',
                                   'short_description', 'product_type', 'origin_country', 'material', 'gender')}),
        (_('Sale'), {'fields': ('sale_price', 'sale_price_start_date', 'sale_price_end_date')}),
        (_('Importer Information'), {'fields': ('importer_name',)}),
        (_('Other'), {'fields': ('pattern', 'visibility', 'start_date')})
    )
