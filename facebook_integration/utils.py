
from django.forms import model_to_dict
import requests

from enum import Enum
from .decorators import timeout, retry_on_connection_error
from .exceptions import AddCatalogItemFailed, DeleteCatalogItemFailed


class GraphAPIUrls(Enum):
    OWNED_PRODUCT_CATALOGS = 'https://graph.facebook.com/v17.0/{business_id}/owned_product_catalogs'
    OWNED_PAGES = 'https://graph.facebook.com/v17.0/{business_id}/owned_pages'
    PRODUCT_CATALOGS_ITEMS = 'https://graph.facebook.com/v17.0/{catalog_id}/products'
    CATALOG_ITEM_ADD = 'https://graph.facebook.com/v17.0/{catalog_id}/products'
    CATALOG_ITEM_DELETE = 'https://graph.facebook.com/v17.0/{product_facebook_id}'
    CATALOG_ITEM_UPDATE = 'https://graph.facebook.com/v17.0/{product_facebook_id}'
    CATALOG_ITEM_READ = 'https://graph.facebook.com/v17.0/{product_facebook_id}'


PRODUCT_FIELDS = ['name', 'description', 'url', 'image_url', 'currency', 'price', 'retailer_id', 'gtin',
                  'condition', 'availability', 'brand', 'category', 'color', 'visibility', 'expiration_date',
                  'additional_image_urls', 'additional_variant_attributes', 'start_date', 'size', 'short_description',
                  'sale_price', 'sale_price_start_date', 'sale_price_end_date', 'product_type', 'pattern',
                  'origin_country', 'material', 'importer_name', 'gender']


class FacebookAdapter:
    def __init__(self, access_token, business_id, catalog_id, page_id):
        self.access_token = access_token
        self.business_id = business_id
        self.catalog_id = catalog_id
        self.page_id = page_id

    @classmethod
    def merchant_facebook_adapter(cls, merchant):
        facebook_integration_data = merchant.facebook_info.decrypted_data()
        return cls(**facebook_integration_data)

    def generate_url(self, url_type: GraphAPIUrls, **kwargs):
        if url_type == GraphAPIUrls.OWNED_PRODUCT_CATALOGS:
            return GraphAPIUrls.OWNED_PRODUCT_CATALOGS.value.format(business_id=self.business_id)
        elif url_type == GraphAPIUrls.OWNED_PAGES:
            return GraphAPIUrls.OWNED_PAGES.value.format(business_id=self.business_id)
        elif url_type == GraphAPIUrls.PRODUCT_CATALOGS_ITEMS:
            return GraphAPIUrls.PRODUCT_CATALOGS_ITEMS.value.format(catalog_id=self.catalog_id)
        elif url_type == GraphAPIUrls.CATALOG_ITEM_ADD:
            return GraphAPIUrls.CATALOG_ITEM_ADD.value.format(catalog_id=self.catalog_id)
        elif url_type == GraphAPIUrls.CATALOG_ITEM_DELETE:
            return GraphAPIUrls.CATALOG_ITEM_DELETE.value.format(product_facebook_id=kwargs.get('facebook_id'))
        elif url_type == GraphAPIUrls.CATALOG_ITEM_UPDATE:
            return GraphAPIUrls.CATALOG_ITEM_UPDATE.value.format(product_facebook_id=kwargs.get('facebook_id'))
        elif url_type == GraphAPIUrls.CATALOG_ITEM_READ:
            return GraphAPIUrls.CATALOG_ITEM_READ.value.format(product_facebook_id=kwargs.get('facebook_id'))
        return None

    def _make_get_request(self, url, query_params=None):
        params = {'access_token': self.access_token}
        if query_params is not None:
            params.update(query_params)
        response = requests.get(url=url, params=params)
        return response

    def _make_post_request(self, url, data, query_params=None):
        params = {'access_token': self.access_token}
        if query_params is not None:
            params.update(query_params)
        response = requests.post(url=url, data=data, params=params)
        return response

    def _make_put_request(self, url, data, query_params=None):
        params = {'access_token': self.access_token}
        if query_params is not None:
            params.update(query_params)
        response = requests.put(url=url, data=data, params=params)
        return response

    def _make_delete_request(self, url):
        params = {'access_token': self.access_token}
        response = requests.delete(url=url, params=params)
        return response

    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=5)
    def get_owned_catalogs(self):
        url = self.generate_url(GraphAPIUrls.OWNED_PRODUCT_CATALOGS)
        response = self._make_get_request(url=url)
        if response.status_code == 200:
            return response.json()
        return None

    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=5)
    def get_owned_pages(self):
        url = self.generate_url(GraphAPIUrls.OWNED_PAGES)
        response = self._make_get_request(url=url)
        if response.status_code == 200:
            return response.json()
        return None

    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=5)
    def get_catalog_items(self, query_fields=None):
        query_fields = PRODUCT_FIELDS if query_fields is None else query_fields
        response = self._make_get_request(
            url=self.generate_url(GraphAPIUrls.PRODUCT_CATALOGS_ITEMS),
            query_params={"fields": ','.join(query_fields)}
        )
        if response.status_code == 200:
            return response.json()['data']
        return {}

    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=5)
    def add_catalog_item(self, product):
        response = self._make_post_request(
            url=self.generate_url(GraphAPIUrls.CATALOG_ITEM_ADD),
            data=product.to_facebook_representation()
        )
        return response

    def bulk_add_catalog_item(self, products):
        added_products = {}
        try:
            for product in products:
                response = self.add_catalog_item(product=product)
                if response.status_code == 200:
                    added_products[product.id] = {'facebook_id': response.json()['id']}
                else:
                    raise AddCatalogItemFailed()
            return added_products
        except AddCatalogItemFailed:
            finished = self._rollback_added_products(added_products=added_products)
            return None

    def _rollback_added_products(self, added_products):
        added_products_facebook_id = [product['facebook_id'] for product in added_products.values()]
        for facebook_id in added_products_facebook_id:
            response = self.remove_catalog_item(facebook_id=facebook_id)
            if response.status_code != 200:
                raise DeleteCatalogItemFailed("Catalog Item Delete Failed")
        return True

    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=5)
    def remove_catalog_item(self, facebook_id):
        url = self.generate_url(url_type=GraphAPIUrls.CATALOG_ITEM_DELETE, facebook_id=facebook_id)
        response = self._make_delete_request(url=url)
        return response

    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=5)
    def update_catalog_item(self, facebook_id, data):
        url = self.generate_url(url_type=GraphAPIUrls.CATALOG_ITEM_UPDATE, facebook_id=facebook_id)
        response = self._make_put_request(
            url=url,
            data=data
        )
        return response

    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=5)
    def get_item_detail(self, facebook_id):
        url = self.generate_url(url_type=GraphAPIUrls.CATALOG_ITEM_READ, facebook_id=facebook_id)
        response = self._make_get_request(url=url)
        return response

    def get_page_detail(self):
        pass

    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=5)
    def verify_info(self):
        owned_pages = self.get_owned_pages()
        owned_catalogs = self.get_owned_catalogs()
        if owned_pages is not None and owned_catalogs is not None:
            owned_pages_id = [page['id'] for page in owned_pages['data']]
            owned_catalogs_id = [catalog['id'] for catalog in owned_catalogs['data']]
            if self.page_id in owned_pages_id and self.catalog_id in owned_catalogs_id:
                return True
        return False
