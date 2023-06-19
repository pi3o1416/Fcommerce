
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    fieldsets = (
        (_('Required Fields'), {'fields': ('name', 'description', 'url', 'image_url', 'currency', 'price', 'retailer_id')}),
        (_('Product'), {'fields': ('condition', 'availability', 'brand', 'category', 'color', 'expiration_date',
                                   'additional_image_urls', 'additional_variant_attributes', 'size',
                                   'short_description', 'product_type', 'origin_country', 'material', 'inventory', 'gender')}),
        (_('Offer'), {'fields': ('offer_price_amount', 'offer_price_start_date', 'offer_price_end_date')}),
        (_('Sale'), {'fields': ('sale_price', 'sale_price_start_date', 'sale_price_end_date')}),
        (_('Importer Information'), {'fields': ('importer_name',)}),
        (_('Other'), {'fields': ('pattern', 'return_policy_days', 'visibility', 'start_date')})
    )