
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.db.models import CheckConstraint
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from dirtyfields import DirtyFieldsMixin

from .validators import UnicodeMerchantNameValidator


class MerchatManager(models.Manager):
    def get_queryset(self):
        return MerchantQuerySet(model=self.model, using=self._db)


class MerchantQuerySet(models.QuerySet):
    pass


class Merchant(DirtyFieldsMixin, models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200,
        unique=True,
        validators=[UnicodeMerchantNameValidator()]
    )
    merchant_id = models.CharField(
        verbose_name=_('Merchant ID'),
        max_length=200,
    )
    password = models.CharField(
        verbose_name=_('Password'),
        max_length=128,
        validators=[validate_password]
    )
    publish_shop = models.BooleanField(
        verbose_name=_('Publish Shop'),
        default=False
    )
    integrate_facebook = models.BooleanField(
        verbose_name=_('Integrate Facebook'),
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
    )
    _password = None

    def set_password(self, raw_password):
        self._password = self.password
        self.password = make_password(password=raw_password)

    def check_password(self, raw_password):
        return check_password(password=raw_password, encoded=self.password)
