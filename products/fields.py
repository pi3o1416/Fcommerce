
import random
from gtin import append_check_digit
from django.db import models
from django.core.exceptions import ValidationError


def generate_gtin_13():
    digits = [random.randint(0, 9) for _ in range(12)]
    gtin_12 = "".join(str(digit) for digit in digits)
    gtin_13 = append_check_digit(gtin_12)
    return gtin_13


def generate_retailer_id():
    digits = [random.randint(0, 9) for _ in range(13)]
    retailer_id = "".join(str(digit) for digit in digits)
    return retailer_id


class AddressJSONField(models.JSONField):
    def __init__(self, *args, **kwargs):
        self.fixed_keys = ['street1', 'street2', 'city', 'region', 'postal_code', 'country']
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value=value, model_instance=model_instance)
        if not isinstance(value, dict):
            raise ValidationError('Value must be a JSON object')
        if set(self.fixed_keys) != set(value.keys()):
            raise ValidationError('Keys does not match with fixed keys')


class GTINField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value:
            value = generate_gtin_13()
            setattr(model_instance, self.attname, value)
        return value


class RetailerIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value:
            value = generate_retailer_id()
            setattr(model_instance, self.attname, value)
        return value
