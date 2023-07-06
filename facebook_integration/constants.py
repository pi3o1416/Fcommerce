
from django.conf import settings
from enum import Enum


GRAPH_API_BASE_URL = f'https://graph.facebook.com/{settings.FACEBOOK_API_VERSION}/'


class GraphAPIUrls(Enum):
    OWNED_PRODUCT_CATALOGS = GRAPH_API_BASE_URL + '{business_id}/owned_product_catalogs'
    OWNED_PAGES = GRAPH_API_BASE_URL + '{business_id}/owned_pages'
    PRODUCT_CATALOGS_ITEMS = GRAPH_API_BASE_URL + '{catalog_id}/products'
    CATALOG_ITEM_ADD = GRAPH_API_BASE_URL + '{catalog_id}/products'
    CATALOG_ITEM_DELETE = GRAPH_API_BASE_URL + '{product_facebook_id}'
    CATALOG_ITEM_UPDATE = GRAPH_API_BASE_URL + '{product_facebook_id}'
    CATALOG_ITEM_READ = GRAPH_API_BASE_URL + '{product_facebook_id}'


PRODUCT_FIELDS = ['name', 'description', 'url', 'image_url', 'currency', 'price', 'retailer_id', 'gtin',
                  'condition', 'availability', 'brand', 'category', 'color', 'visibility', 'expiration_date',
                  'additional_image_urls', 'additional_variant_attributes', 'start_date', 'size', 'short_description',
                  'sale_price', 'sale_price_start_date', 'sale_price_end_date', 'product_type', 'pattern',
                  'origin_country', 'material', 'importer_name', 'gender']
