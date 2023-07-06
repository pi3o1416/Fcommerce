
from django.forms import model_to_dict
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from dirtyfields import DirtyFieldsMixin
from rest_framework.exceptions import ValidationError

from .utils import FacebookAdapter
from crypto.fernet import decrypt_data

Merchant = get_user_model()


class FacebookIntegrationData(DirtyFieldsMixin, models.Model):
    merchant = models.OneToOneField(
        verbose_name=_('Merchant'),
        to=Merchant,
        on_delete=models.CASCADE,
        related_name='facebook_info',
        unique=True,
    )
    access_token = models.CharField(
        verbose_name=_('Access Token'),
        max_length=700,
        unique=True,
    )
    business_id = models.CharField(
        verbose_name=_('Business ID'),
        max_length=500,
        unique=True,
    )
    catalog_id = models.CharField(
        verbose_name=_('Catalog ID'),
        max_length=500,
        unique=True,
    )
    page_id = models.CharField(
        verbose_name=_('Page ID'),
        max_length=500,
        unique=True,
    )
    page_data = models.JSONField(
        verbose_name=_('Page Info'),
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        facebook_adapter = FacebookAdapter(
            merchant=self.merchant,
            access_token=self.access_token,
            business_id=self.business_id,
            catalog_id=self.catalog_id,
            page_id=self.page_id
        )
        if facebook_adapter.verify_info() is False:
            raise ValidationError('Facebook Integration Data Verification Failed')
        super().save(*args, **kwargs)

    def decrypted_data(self):
        encrypted_data = model_to_dict(self)
        decrypted_data = {}
        for key, value in encrypted_data.items():
            if type(value) is str:
                decrypted_data[key] = decrypt_data(value)
        return decrypted_data
