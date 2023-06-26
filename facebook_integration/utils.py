
import requests

from enum import Enum
from products.models import Product


class URLType(Enum):
    OWNED_PRODUCT_CATALOGS = 'https://graph.facebook.com/v17.0/{}/owned_product_catalogs'
    OWNED_PAGES = 'https://graph.facebook.com/v17.0/{}/owned_pages'
    PRODUCT_CATALOGS_ITEMS = 'https://graph.facebook.com/v17.0/{}/products'
    CATALOG_ITEM_ADD = 'https://graph.facebook.com/v17.0/{}/products'
    CATALOG_ITEM_DELETE = 'https://graph.facebook.com/v17.0/{}'
    CATALOG_ITEM_UPDATE = 'https://graph.facebook.com/v17.0/{}'
    CATALOG_ITEM_READ = 'https://graph.facebook.com/v17.0/{}'


class FacebookAdapter:
    def __init__(self, access_token, business_id, catalog_id, page_id):
        self.access_token = access_token
        self.business_id = business_id
        self.catalog_id = catalog_id
        self.page_id = page_id

    def generate_url(self, url_type: URLType, **kwargs):
        if url_type == URLType.OWNED_PRODUCT_CATALOGS:
            return URLType.OWNED_PRODUCT_CATALOGS.value.format(self.business_id)
        elif url_type == URLType.OWNED_PAGES:
            return URLType.OWNED_PAGES.value.format(self.business_id)
        elif url_type == URLType.PRODUCT_CATALOGS_ITEMS:
            return URLType.PRODUCT_CATALOGS_ITEMS.value.format(self.catalog_id)
        elif url_type == URLType.CATALOG_ITEM_ADD:
            return URLType.CATALOG_ITEM_ADD.value.format(self.catalog_id)
        elif url_type == URLType.CATALOG_ITEM_DELETE:
            return URLType.CATALOG_ITEM_DELETE.value.format(kwargs.get('facebook_id'))
        elif url_type == URLType.CATALOG_ITEM_UPDATE:
            return URLType.CATALOG_ITEM_UPDATE.value.format(kwargs.get('facebook_id'))
        elif url_type == URLType.CATALOG_ITEM_READ:
            return URLType.CATALOG_ITEM_READ.value.format(kwargs.get('facebook_id'))
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

    def get_owned_catalogs(self):
        url = self.generate_url(URLType.OWNED_PRODUCT_CATALOGS)
        response = self._make_get_request(url=url)
        if response.status_code == 200:
            return response.json()
        return None

    def get_owned_pages(self):
        url = self.generate_url(URLType.OWNED_PAGES)
        response = self._make_get_request(url=url)
        if response.status_code == 200:
            return response.json()
        return None

    def get_catalog_items(self):
        product_fields = [field.name for field in Product._meta.fields if field.name not in ['facebook_id']]
        response = self._make_get_request(
            url=self.generate_url(URLType.PRODUCT_CATALOGS_ITEMS),
            query_params={"fields": ','.join(product_fields)}
        )
        if response.status_code == 200:
            return response.json()
        return None

    def add_catalog_item(self, data):
        response = self._make_post_request(
            url=self.generate_url(URLType.CATALOG_ITEM_ADD),
            data=data
        )
        return response

    def remove_catalog_item(self, facebook_id):
        url = self.generate_url(url_type=URLType.CATALOG_ITEM_DELETE, facebook_id=facebook_id)
        response = self._make_delete_request(url=url)
        return response

    def update_catalog_item(self, facebook_id, data):
        url = self.generate_url(url_type=URLType.CATALOG_ITEM_UPDATE, facebook_id=facebook_id)
        response = self._make_put_request(
            url=url,
            data=data
        )
        return response

    def get_item_detail(self, facebook_id):
        url = self.generate_url(url_type=URLType.CATALOG_ITEM_READ, facebook_id=facebook_id)
        response = self._make_get_request(url=url)
        return response

    def get_page_detail(self):
        pass

    def verify_info(self):
        owned_pages = self.get_owned_pages()
        owned_catalogs = self.get_owned_catalogs()
        if owned_pages is not None and owned_catalogs is not None:
            owned_pages_id = [page['id'] for page in owned_pages['data']]
            owned_catalogs_id = [catalog['id'] for catalog in owned_catalogs['data']]
            if self.page_id in owned_pages_id and self.catalog_id in owned_catalogs_id:
                return True
        return False
