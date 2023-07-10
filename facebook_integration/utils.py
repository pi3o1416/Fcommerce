
import logging
import requests
from decimal import Decimal

from .decorators import timeout, retry_on_connection_error, log_api_errors
from .exceptions import AddCatalogItemFailed, BulkProductAddFailed, DeleteCatalogItemFailed, UpdateCatalogItemFailed
from .constants import PRODUCT_FIELDS, GraphAPIUrls


logger = logging.getLogger('facebook_api_error_logger')


class FacebookAdapter:
    def __init__(self, merchant, access_token, business_id, catalog_id, page_id):
        self.merchant = merchant
        self.access_token = access_token
        self.business_id = business_id
        self.catalog_id = catalog_id
        self.page_id = page_id

    @classmethod
    def merchant_facebook_adapter(cls, merchant):
        facebook_integration_data = merchant.facebook_info.decrypted_data()
        return cls(**facebook_integration_data, merchant=merchant)

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

    @log_api_errors
    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=10)
    def get_owned_catalogs(self, create_notification=True):
        url = self.generate_url(GraphAPIUrls.OWNED_PRODUCT_CATALOGS)
        response = self._make_get_request(url=url)
        if response.status_code == 200:
            return response.json()
        return None

    @log_api_errors
    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=10)
    def get_owned_pages(self):
        url = self.generate_url(GraphAPIUrls.OWNED_PAGES)
        response = self._make_get_request(url=url)
        if response.status_code == 200:
            return response.json()
        return None

    @log_api_errors
    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=10)
    def get_catalog_items(self, query_fields=None):
        query_fields = PRODUCT_FIELDS if query_fields is None else query_fields
        response = self._make_get_request(
            url=self.generate_url(GraphAPIUrls.PRODUCT_CATALOGS_ITEMS),
            query_params={"fields": ','.join(query_fields)}
        )
        if response.status_code == 200:
            return self._format_facebook_product_data(response.json()['data'])
        return None

    @log_api_errors
    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=10)
    def add_catalog_item(self, product):
        response = self._make_post_request(
            url=self.generate_url(GraphAPIUrls.CATALOG_ITEM_ADD),
            data=self._format_product_data_for_facebook(product=product)
        )
        if response.status_code != 200:
            raise AddCatalogItemFailed(response=response)
        return response

    @log_api_errors
    def bulk_add_catalog_item(self, products):
        added_products = {}
        try:
            for product in products:
                response = self.add_catalog_item(product=product)
                added_products[product.id] = {'facebook_id': response.json()['id']}
            return added_products
        except AddCatalogItemFailed as exception:
            self._rollback_added_products(added_products=added_products, exception_message=exception.__str__())
            raise BulkProductAddFailed(response=exception.response)

    def _rollback_added_products(self, added_products, exception_message=None):
        added_products_facebook_id = [product['facebook_id'] for product in added_products.values()]
        for facebook_id in added_products_facebook_id:
            self.remove_catalog_item(facebook_id=facebook_id)

    @log_api_errors
    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=10)
    def remove_catalog_item(self, facebook_id):
        url = self.generate_url(url_type=GraphAPIUrls.CATALOG_ITEM_DELETE, facebook_id=facebook_id)
        response = self._make_delete_request(url=url)
        if response.status_code != 200:
            raise DeleteCatalogItemFailed(response=response)
        return response

    @log_api_errors
    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=10)
    def update_catalog_item(self, product):
        response = self._make_post_request(
            url=self.generate_url(url_type=GraphAPIUrls.CATALOG_ITEM_UPDATE, facebook_id=product.facebook_id),
            data=self._format_product_data_for_facebook(product=product)
        )
        print(response.json())
        if response.status_code != 200:
            raise UpdateCatalogItemFailed(response=response)
        return response

    @log_api_errors
    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=10)
    def get_item_detail(self, facebook_id):
        url = self.generate_url(url_type=GraphAPIUrls.CATALOG_ITEM_READ, facebook_id=facebook_id)
        response = self._make_get_request(url=url)
        return response

    def get_page_detail(self):
        pass

    @log_api_errors
    @retry_on_connection_error(number_of_retry=5)
    @timeout(seconds=10)
    def verify_info(self):
        owned_pages = self.get_owned_pages()
        owned_catalogs = self.get_owned_catalogs()
        if owned_pages is not None and owned_catalogs is not None:
            owned_pages_id = [page['id'] for page in owned_pages['data']]
            owned_catalogs_id = [catalog['id'] for catalog in owned_catalogs['data']]
            if self.page_id in owned_pages_id and self.catalog_id in owned_catalogs_id:
                return True
        return False

    @staticmethod
    def _format_facebook_product_price(price):
        if price is not None:
            price = price[1:]
            return ''.join(price.split(','))
        return None

    @staticmethod
    def _format_inventory_product_price(price):
        if price is not None:
            decimal_price = Decimal(price) * Decimal('100')
            return int(decimal_price)
        return None

    @staticmethod
    def _format_facebook_product_data(facebook_product_data: dict):
        """
        Format Facebook data for future use
        """
        for product_data in facebook_product_data:
            facebook_id = product_data.pop('id')
            product_data['price'] = FacebookAdapter._format_facebook_product_price(product_data.get('price'))
            product_data['sale_price'] = FacebookAdapter._format_facebook_product_price(product_data.get('sale_price'))
            product_data['facebook_id'] = facebook_id
        return facebook_product_data

    @staticmethod
    def _format_product_data_for_facebook(product):
        """
        Dictionary used to format product data on facebook graph api
        """
        product_data = product.__dict__.copy()
        product_data.pop('id')
        product_data['price'] = FacebookAdapter._format_inventory_product_price(product_data.get('price'))
        product_data['sale_price'] = FacebookAdapter._format_inventory_product_price(product_data.get('sale_price'))
        return product_data
