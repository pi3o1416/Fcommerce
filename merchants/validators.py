
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class UnicodeMerchantNameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Enter a valid merchant name. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0
