
import random
from django.db import models
from django.core.exceptions import ValidationError


def generate_gtin_13():
    digits = [random.randint(0, 9) for _ in range(12)]
    check_digit = calculate_check_digit(digits)
    gtin_13 = "".join(str(d) for d in digits) + str(check_digit)
    return gtin_13


def calculate_check_digit(digits):
    # Multiply each digit by 3 or 1 based on its position
    weighted_sum = sum(d * (3 if i % 2 == 0 else 1) for i, d in enumerate(digits))
    # Calculate the check digit as the nearest equal or higher multiple of 10
    check_digit = (10 - (weighted_sum % 10)) % 10
    return check_digit


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
