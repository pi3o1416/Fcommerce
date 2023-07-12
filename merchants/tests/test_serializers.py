
import uuid
from django.test import TestCase
from ..serializers import MerchantCreateSerializer, MerchantUpdateSerializer


class TestMerchantCreateSerializer(TestCase):
    def setUp(self):
        self.merchant_create_data = {
            "name": "testmerchant",
            "merchant_id": "testmerchant",
            "signature_key": uuid.uuid4().hex,
            "password": "testtestap1",
            "retype_password": "testtestap1"
        }

    @staticmethod
    def initialize_serializer(data):
        serializer = MerchantCreateSerializer(data=data)
        serializer.is_valid()
        return serializer

    def _test_absent_field(self, field_name):
        merchant_data = self.merchant_create_data.copy()
        del merchant_data[field_name]
        serializer = self.initialize_serializer(data=merchant_data)
        self.assertFalse(serializer.is_valid(), f"{field_name} absent should not be acceptable")

    def test_valid_serializer(self):
        merchant_data = self.merchant_create_data.copy()
        serializer = self.initialize_serializer(data=merchant_data)
        self.assertTrue(serializer.is_valid(), "Serializer should be valid for valid data")

    def test_invalid_password(self):
        merchant_data = self.merchant_create_data.copy()
        merchant_data['password'], merchant_data['retype_password'] = '1234', '1234'
        serializer = self.initialize_serializer(data=merchant_data)
        self.assertFalse(serializer.is_valid(), "Serializer validation should be false for invalid password")

    def test_password_mismatch(self):
        merchant_data = self.merchant_create_data.copy()
        merchant_data['retype_password'] = 'testtestapc1'
        serializer = self.initialize_serializer(data=merchant_data)
        self.assertFalse(serializer.is_valid(), "Serializer validation should be false for password mismatch")

    def test_absent_name_field(self):
        self._test_absent_field(field_name='name')

    def test_absent_merchant_id_field(self):
        self._test_absent_field(field_name='merchant_id')

    def test_absent_password_field(self):
        self._test_absent_field(field_name='password')

    def test_absent_retype_password_field(self):
        self._test_absent_field(field_name='retype_password')


class TestMerchantUpdateSerializer(TestCase):
    def setUp(self):
        self.merchant_update_data = {
            'name': 'testmerchant',
            'publish_shop': True
        }
        pass

    @staticmethod
    def initialize_serializer(data):
        serializer = MerchantUpdateSerializer(data=data)
        serializer.is_valid()
        return serializer

    def _test_absent_field(self, field_name):
        merchant_data = self.merchant_update_data.copy()
        del merchant_data[field_name]
        serializer = self.initialize_serializer(data=merchant_data)
        self.assertFalse(serializer.is_valid(), f"{field_name} absent should not be acceptable")

    def test_absent_name_field(self):
        self._test_absent_field(field_name='name')
