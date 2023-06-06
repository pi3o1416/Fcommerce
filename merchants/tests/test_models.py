
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from ..models import Merchant


class TestMerchant(TestCase):
    def setUp(self):
        self.merchant_data = {
            "name": "fcommerce",
            "merchant_id": "fcommerce",
            "password": "testtestap1"
        }
        Merchant.objects.create(**self.merchant_data)

    def test_merchant_create_successful(self):
        try:
            merchant = Merchant.objects.get(name='fcommerce')
        except Merchant.DoesNotExist:
            merchant = None
        finally:
            self.assertIsNotNone(merchant, "Merchat is not created")

    def test_unique_name(self):
        created = None
        try:
            new_merchant_data = self.merchant_data.copy()
            new_merchant_data['merchant_id'] = 'fcommerce_new'
            Merchant.objects.create(**new_merchant_data)
            created = True
        except IntegrityError:
            created = False
        finally:
            self.assertFalse(created, "Merchant should not be created for duplicate name")

    def test_unique_merchant_id(self):
        created = None
        try:
            new_merchant_data = self.merchant_data.copy()
            new_merchant_data['name'] = 'fcommerce_new'
            Merchant.objects.create(**new_merchant_data)
            created = True
        except IntegrityError:
            created = False
        finally:
            self.assertFalse(created, "Merchant should not be created for duplicate merchant id")

    def test_unicode_name_validator(self):
        updated = None
        try:
            merchant = Merchant.objects.get(name='fcommerce')
            merchant.name = 'fcommerce#%^&'
            merchant.clean_fields()
            merchant.save()
            updated = True
        except ValidationError:
            updated = False
        finally:
            self.assertFalse(updated, "Name field Updated should be blocked by validation Error")

    def test_name_max_length(self):
        max_length = Merchant._meta.get_field('name').max_length
        self.assertEqual(max_length, 200, "Name field max length should be 200")

    def test_merchant_id_max_length(self):
        max_length = Merchant._meta.get_field('merchant_id').max_length
        self.assertEqual(max_length, 200, "Merchant_id max length should be 200")

    def test_set_password(self):
        pass

    def test_check_password(self):
        password = self.merchant_data['password']
        merchant = Merchant.objects.get(name='fcommerce')
        matched = merchant.check_password(password)
        self.assertTrue(matched, "Password should be matched with raw password")

    def test_password_encrypt_signal(self):
        pass

    def test_publish_shop_default(self):
        pass

    def test_integrate_facebook_default(self):
        pass
