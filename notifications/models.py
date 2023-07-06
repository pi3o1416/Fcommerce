
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models


Merchant = get_user_model()


class FacebookAPIErrorLog(models.Model):
    merchant = models.ForeignKey(
        to=Merchant,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    api_response_status_code = models.IntegerField(
        verbose_name=_('Response Status Code'),
        null=True,
        blank=True
    )
    api_response = models.JSONField(
        verbose_name=_('API Response'),
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True
    )
    message = models.CharField(
        verbose_name=_("Message"),
        null=True,
        blank=True
    )
