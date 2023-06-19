
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class ExpirationDateValidator:
    def __call__(self, expiration_date):
        current_date = timezone.now().date()
        if current_date >= expiration_date:
            raise ValidationError("Expiration date should be greater than current date")
        return expiration_date
