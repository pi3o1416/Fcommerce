
import random
from gtin import has_valid_check_digit
from iso4217 import raw_table
from django.test import TestCase
from django.db.models.fields import URLField
from django.utils import timezone
from ..models import Product


class ProductTest(TestCase):
    def setUp(self):
        self.retailer_id = self.generate_retailer_id()
        self.product_data = {
            "name": "Test Product",
            "description": "Test Product Description",
            "url": "www.example.com",
            "image_url": "www.example.com/image.png",
            "currency": "BDT",
            "price": "123",
            "retailer_id": self.retailer_id
        }
        self.create_product(self.product_data)

    @staticmethod
    def generate_retailer_id():
        return random.randint(1, 999999999999)

    @staticmethod
    def _validate_currencies(currencies):
        for currency in currencies:
            if currency.upper() not in raw_table.keys():
                return False
        return True

    @staticmethod
    def _validate_choices(expected_choices, actual_choices):
        if len(actual_choices) != len(expected_choices):
            return False
        for choice in expected_choices:
            if choice not in actual_choices:
                return False
        return True

    @classmethod
    def create_product(cls, product_data):
        try:
            product = Product.objects.create(**product_data)
            return product
        except Exception:
            return None

    @classmethod
    def create_product_with_retailer_id(cls, product_data, absent_field=None):
        try:
            if absent_field and absent_field in product_data:
                product_data[absent_field] = None
            product_data['retailer_id'] = cls.generate_retailer_id()
            product = cls.create_product(product_data=product_data)
            return product
        except Exception:
            return None

    def test_successful_product_create(self):
        product = Product.objects.filter(retailer_id=self.retailer_id).first()
        self.assertIsNotNone(product, "Product should be found with retailer id")

    def test_accepted_currency_choice(self):
        currency_choices = [currency[0] for currency in Product.AcceptedCurrency.choices]
        is_valid = self._validate_currencies(currencies=currency_choices)
        self.assertTrue(is_valid, "Currency is not exist in ISO 4217")

    def test_condition_choices(self):
        expected_choices = ["new", "refurbished", "used", "used_like_new", "used_good", "used_fair", "cpo", "open_box_new"]
        actual_choices = [choice[0] for choice in Product.ConditionChoices.choices]
        is_valid = self._validate_choices(expected_choices=expected_choices, actual_choices=actual_choices)
        self.assertTrue(is_valid, "Condition choices did not match with facebook condition choices")

    def test_availability_choices(self):
        expected_choices = ["in stock", "out of stock", "preorder", "available for order", "discontinued", "pending"]
        actual_choices = [choice[0] for choice in Product.AvailabilityChoices.choices]
        is_valid = self._validate_choices(expected_choices=expected_choices, actual_choices=actual_choices)
        self.assertTrue(is_valid, "Availability choices did not match with facebook available choices")

    def test_visibility_choices(self):
        expected_choices = ["staging", "published"]
        actual_choices = [choice[0] for choice in Product.VisibilityChoices.choices]
        is_valid = self._validate_choices(expected_choices=expected_choices, actual_choices=actual_choices)
        self.assertTrue(is_valid, "Visibility choices did not match with facebook visibility choices")

    def test_gender_choices(self):
        expected_choices = ["female", "male", "unisex"]
        actual_choices = [choice[0] for choice in Product.GenderChoices.choices]
        is_valid = self._validate_choices(expected_choices=expected_choices, actual_choices=actual_choices)
        self.assertTrue(is_valid, "Gender choices did not match with facebook gender choices")

    def test_null_restriction_on_name_field(self):
        product = self.create_product_with_retailer_id(self.product_data.copy(), 'name')
        self.assertIsNone(product, "Product creation should not be allowed without name")

    def test_null_restriction_on_description_field(self):
        product = self.create_product_with_retailer_id(self.product_data.copy(), 'description')
        self.assertIsNone(product, "Product creation should not be allowed without description")

    def test_null_restriction_on_url_field(self):
        product = self.create_product_with_retailer_id(self.product_data.copy(), 'url')
        self.assertIsNone(product, "Product creation should not be allowed without url")

    def test_invalid_url_on_url_field(self):
        field = Product._meta.get_field('url')
        self.assertTrue(isinstance(field, URLField), 'URL should be an instance of url field')

    def test_null_restriction_on_image_url_field(self):
        product = self.create_product_with_retailer_id(self.product_data.copy(), 'image_url')
        self.assertIsNone(product, "Product creation should not be allowed without image url")

    def test_invalid_url_on_image_url_field(self):
        field = Product._meta.get_field('image_url')
        self.assertTrue(isinstance(field, URLField), 'Image URL should be an instance of url field')

    def test_null_restriction_on_currency_field(self):
        product = self.create_product_with_retailer_id(self.product_data.copy(), 'currency')
        self.assertIsNone(product, "Product creation should not be allowed without currency")

    def test_invalid_currency_code_not_supported_by_ISO_4217(self):
        pass

    def test_null_restriction_on_price_field(self):
        product = self.create_product_with_retailer_id(self.product_data.copy(), 'price')
        self.assertIsNone(product, "Product creation should not be allowed without image url")

    def test_negetive_value_on_price_field(self):
        product_data = self.product_data.copy()
        product_data['price'] = -10
        product = self.create_product(product_data=product_data)
        self.assertIsNone(product, 'Product create with negative price should not be allowed')

    def test_unique_constraint_on_retailer_id(self):
        product_data = self.product_data.copy()
        product = self.create_product(product_data)
        self.assertIsNone(product, "Product creation should not be allowed with duplicate retailer id")

    def test_auto_generation_of_gtin_field(self):
        product = Product.objects.get(retailer_id=self.retailer_id)
        gtin = product.gtin
        self.assertIsNotNone(gtin, 'GTIN value should not be null')
        self.assertTrue(has_valid_check_digit(gtin=gtin), "generated gtin should be valid")

    def test_invlaid_condition_not_supported_by_facebook(self):
        condition_choices = Product._meta.get_field('condition').choices
        self.assertEqual(condition_choices, Product.ConditionChoices.choices, "Product condition choices did not match")

    def test_invalid_availability_not_supported_by_facebook(self):
        availability_choices = Product._meta.get_field('availability').choices
        self.assertEqual(availability_choices, Product.AvailabilityChoices.choices, 'Product availability choices did not match')

    def test_invalid_visibility_not_supported_by_facebook(self):
        visibility_choices = Product._meta.get_field('visibility').choices
        self.assertEqual(visibility_choices, Product.VisibilityChoices.choices, 'Product Visibility choices did not match')

    def test_invalid_gender_supported_by_facebook(self):
        gender_choices = Product._meta.get_field('gender').choices
        self.assertEqual(gender_choices, Product.GenderChoices.choices, 'Product gender choice did not match')

    def test_expiration_date_in_valid_range(self):
        product_data = self.product_data.copy()
        product_data['expiration_date'] = timezone.now().date() - timezone.timedelta(days=2)
        product = self.create_product_with_retailer_id(product_data=product_data)
        self.assertIsNone(product, 'Past date on expiration date should not be allowed')
