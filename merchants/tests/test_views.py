
from urllib.parse import urlencode
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from ..models import Merchant


class MerchantViewSetTest(TestCase):
    def setUp(self) -> None:
        self.merchants_data = [
            {
                'name': 'testmerchant1',
                'merchant_id': 'testmerchant1',
                'password': 'testpassword1',
            },
            {
                'name': 'testmerchant2',
                'merchant_id': 'testmerchant2',
                'password': 'testpassword2',
            },
            {
                'name': 'testmerchant3',
                'merchant_id': 'testmerchant3',
                'password': 'testpassword3'
            }
        ]
        Merchant.objects.bulk_create([Merchant(**merchant_data) for merchant_data in self.merchants_data])
        return super().setUp()

    @staticmethod
    def get_response(view_name, method='get', data=None, query_params={}):
        url = f'{reverse(view_name)}?{urlencode(query_params)}'
        client = Client()
        response = getattr(client, method)(url, data)
        return response

    @staticmethod
    def get_list_view_response(query_params={}):
        response = MerchantViewSetTest.get_response('merchant:merchant-list', query_params=query_params)
        return response

    @staticmethod
    def get_create_view_response(data):
        response = MerchantViewSetTest.get_response('merchant:merchant-list', method='post', data=data)
        return response

    def test_list_view_status_code(self):
        response = self.get_list_view_response()
        self.assertEqual(response.status_code, 200, 'Status code should be 200')

    def test_list_view_success_message(self):
        response = self.get_list_view_response()
        self.assertEqual(response.data['message'], 'Merchant List')

    def test_list_view_response_dict(self):
        response = self.get_list_view_response()
        self.assertEqual(set(response.data.keys()), {'detail', 'message'}, 'message and detail key absent from response')

    def test_list_view_pagination(self):
        response = self.get_list_view_response()
        response_data = response.data['detail']
        self.assertEqual(set(response_data.keys()), {'count', 'next', 'previous', 'results'}, 'Response is not paginated')

    def test_list_view_without_page_size_query_param(self):
        response = self.get_list_view_response()
        merchant_count = len(response.data['detail']['results'])
        self.assertEqual(merchant_count, len(self.merchants_data), 'Merchant count should be 3 without ')

    def test_list_view_with_page_size_query_param(self):
        response = self.get_list_view_response(query_params={'page_size': 1})
        merchant_count = len(response.data['detail']['results'])
        self.assertEqual(merchant_count, 1, 'Merchant count should be 1 since page size 1')

    def test_create_view_status_code(self):
        merchant_data = self.merchants_data[0].copy()
        merchant_data['name'] = 'testmerchant4'
        merchant_data['merchant_id'] = 'testmerchant4'
        resopnse = self.get_create_view_response(data=merchant_data)

    def test_create_view_duplicate_merchant_id(self):
        pass

    def test_create_view_duplicate_name(self):
        pass

    def test_create_view_incorrect_password(self):
        pass

    def test_create_view_in_database_level(self):
        pass

    def test_create_view_success_message(self):
        pass

    def test_create_view_fail_message(self):
        pass

    def test_create_view_response_data(self):
        pass

    def test_retrieve_view_status_code(self):
        pass

    def test_retrieve_view_fail_status_code(self):
        pass

    def test_retrieve_view_response(self):
        pass

    def test_retrieve_view_success_message(self):
        pass

    def test_retrieve_view_fail_message(self):
        pass

    def test_destroy_view_status_code(self):
        pass

    def test_destroy_view_success_message(self):
        pass

    def test_destroy_view_fail_status_code(self):
        pass

    def test_destroy_view_fail_message(self):
        pass
