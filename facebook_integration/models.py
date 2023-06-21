
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from dirtyfields import DirtyFieldsMixin

Merchant = get_user_model()


class FacebookIntegrationData(DirtyFieldsMixin, models.Model):
    merchant = models.ForeignKey(
        verbose_name=_('Merchant'),
        to=Merchant,
        on_delete=models.CASCADE,
        related_name='facebook_info'
    )
    access_token = models.CharField(
        verbose_name=_('Access Token'),
        max_length=700,
    )
    business_id = models.CharField(
        verbose_name=_('Business ID'),
        max_length=500
    )
    catalog_id = models.CharField(
        verbose_name=_('Catalog ID'),
        max_length=500
    )
    page_id = models.CharField(
        verbose_name=_('Page ID'),
        max_length=500
    )
    page_data = models.JSONField(
        verbose_name=_('Page Info'),
        null=True,
        blank=True
    )
