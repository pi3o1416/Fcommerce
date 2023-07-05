
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from products.tasks import sync_inventory_with_facebook
from crypto.fernet import encrypt_data
from .models import FacebookIntegrationData


@receiver(signal=pre_save, sender=FacebookIntegrationData)
def encrypt_facebook_data(sender, instance: FacebookIntegrationData, **kwargs):
    dirty_fields = instance.get_dirty_fields()
    for field in dirty_fields:
        current_value = getattr(instance, field)
        if type(current_value) is str:
            new_value = encrypt_data(current_value)
            setattr(instance, field, new_value)
    return instance


@receiver(signal=post_save, sender=FacebookIntegrationData)
def set_merchant_integration_status_true(sender, instance: FacebookIntegrationData, **kwargs):
    merchant = instance.merchant
    merchant.integrate_facebook = True
    merchant.save()


@receiver(signal=post_delete, sender=FacebookIntegrationData)
def set_merchant_integration_status_false(sender, instance: FacebookIntegrationData, **kwargs):
    merchant = instance.merchant
    merchant.integrate_facebook = False
    merchant.save()


@receiver(signal=post_save, sender=FacebookIntegrationData)
def sync_inventory_with_facebook_on_integration(sender, instance: FacebookIntegrationData, created, **kwargs):
    if created:
        sync_inventory_with_facebook.delay(instance.merchant_id)
