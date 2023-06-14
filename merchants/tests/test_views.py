
from urllib.parse import urlencode
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from services.constants import ErrorTypes
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
    def get_response(view_name, method='get', data=None, query_params={}, kwargs=None):
        url = f'{reverse(view_name, kwargs=kwargs)}?{urlencode(query_params)}'
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

    @staticmethod
    def get_retrieve_view_response(merchant_id):
        response = MerchantViewSetTest.get_response('merchant:merchant-detail', method='get', kwargs={'id': merchant_id})
        return response

    @staticmethod
    def get_destroy_view_response(merchant_id):
        response = MerchantViewSetTest.get_response('merchant:merchant-detail', method='delete', kwargs={'id': merchant_id})
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

    def test_create_view_status_code_and_success_message(self):
        merchant_data = self.merchants_data[0].copy()
        merchant_data['name'] = 'testmerchant4'
        merchant_data['merchant_id'] = 'testmerchant4'
        merchant_data['retype_password'] = merchant_data['password']
        response = self.get_create_view_response(data=merchant_data)
        self.assertEqual(response.status_code, 201, 'Merchant Status status code should be 201')
        self.assertEqual(response.data['message'], 'Merchant Create Successful', 'Invalid merchant create success message')

    def test_create_view_duplicate_merchant_id(self):
        merchant_data = self.merchants_data[0].copy()
        merchant_data['name'] = 'testmerchant5'
        response = self.get_create_view_response(data=merchant_data)
        self.assertEqual(response.status_code, 400, 'Merchant create status code should be 400 for duplicate merchant_id')
        self.assertTrue('merchant_id' in response.data['detail'], 'merchant_id should be in Error data')

    def test_create_view_duplicate_name(self):
        merchant_data = self.merchants_data[0].copy()
        merchant_data['merchant_id'] = 'testmerchant5'
        response = self.get_create_view_response(data=merchant_data)
        self.assertEqual(response.status_code, 400, 'Merchant create status code should be 400 for duplicate name')
        self.assertTrue('name' in response.data['detail'], 'name should be in Error data')

    def test_create_view_incorrect_password(self):
        merchant_data = self.merchants_data[0].copy()
        merchant_data['password'] = '1234'
        merchant_data['retype_password'] = merchant_data['password']
        response = self.get_create_view_response(data=merchant_data)
        self.assertEqual(response.status_code, 400, 'Merchant create status code should be 400 for invalid password')
        self.assertTrue('password' in response.data['detail'], 'password should be in Error data')

    def test_create_view_mismatch_password_and_retype_password(self):
        merchant_data = self.merchants_data[0].copy()
        merchant_data['password'] = 'testtsetap1'
        merchant_data['retype_password'] = 'testtestap2'
        response = self.get_create_view_response(data=merchant_data)
        self.assertEqual(response.status_code, 400, 'Merchant create status code should be 400 for mismatch password')
        self.assertTrue('retype_password' in response.data['detail'], 'password should be in Error data')

    def test_create_view_error_type(self):
        merchant_data = self.merchants_data[0].copy()
        response = self.get_create_view_response(data=merchant_data)
        self.assertTrue(response.data['error_type'] == ErrorTypes.FORM_FIELD_ERROR.value, 'Error type for merchant create invalid')

    def test_create_view_in_database_level(self):
        merchant_data = {
            'name': 'testmerchant10',
            'merchant_id': 'testmerchant10',
            'password': 'merchant10merchant10',
            'retype_password': 'merchant10merchant10'
        }
        response = self.get_create_view_response(data=merchant_data)
        merchant = Merchant.objects.filter(name='testmerchant10').first()
        self.assertEqual(response.status_code, 201, 'Response code for successful merchant create should be 201')
        self.assertIsNotNone(merchant, 'Merchant data not found in database')
        if merchant is not None:
            self.assertTrue(merchant.name == 'testmerchant10', 'name did not match')
            self.assertTrue(merchant.merchant_id == 'testmerchant10', 'merchant_id did not match')
            self.assertTrue(merchant.check_password('merchant10merchant10'), 'password is not ecrtypted')
            self.assertTrue(merchant.is_staff is False, 'is_staff did not match')
            self.assertTrue(merchant.is_superuser is False, 'is_superuser did not match')
            self.assertTrue(merchant.is_active is True, 'is_active did not match')

    def test_create_view_fail_message(self):
        merchant_data = self.merchants_data[0].copy()
        response = self.get_create_view_response(data=merchant_data)
        self.assertEqual(response.data['message'], 'Merchant Account Create Failed', 'Invalid Merchant Create faield message')

    def test_retrieve_view_status_code(self):
        merchant = Merchant.objects.all().first()
        response = self.get_retrieve_view_response(merchant_id=merchant.id)
        self.assertEqual(response.status_code, 200, 'Merchant account retrieve status code should be 200')

    def test_retrieve_view_fail_status_code(self):
        response = self.get_retrieve_view_response(merchant_id='tset')
        self.assertEqual(response.status_code, 404, 'Merchant account retrieve failed status code should be 404')

    def test_retrieve_view_success_message(self):
        merchant = Merchant.objects.all().first()
        response = self.get_retrieve_view_response(merchant_id=merchant.id)
        self.assertEqual(response.data['message'], 'Merchant Retrieved')

    def test_retrieve_view_fail_message(self):
        response = self.get_retrieve_view_response(merchant_id='tset')
        self.assertEqual(response.data['message'], 'Merchant Account Not Found', 'Merchant account retrieve failed message did not match')

    def test_destroy_view_status_code(self):
        merchant = Merchant.objects.all().first()
        response = self.get_destroy_view_response(merchant_id=merchant.id)
        self.assertEqual(response.status_code, 204, 'Merchant Account Destroy status code did not match')

    def test_destroy_view_success_message(self):
        merchant = Merchant.objects.all().first()
        response = self.get_destroy_view_response(merchant_id=merchant.id)
        self.assertEqual(response.data['message'], 'Merchant Deleted')
