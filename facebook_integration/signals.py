
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from products.models import Product
from crypto.fernet import encrypt_data
from .utils import FacebookAdapter
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
def retrieve_existed_products(sender, instance: FacebookIntegrationData, **kwargs):
    # TODO: Move this signal to a celery task
    decrypted_data = instance.decrypted_data()
    facebook_adapter = FacebookAdapter(
        access_token=decrypted_data['access_token'],
        business_id=decrypted_data['business_id'],
        catalog_id=decrypted_data['catalog_id'],
        page_id=decrypted_data['page_id']
    )
    facebook_products = facebook_adapter.get_catalog_items()
    if facebook_products is not None:
        retailer_ids = [product['retailer_id'] for product in facebook_products['data']]
        merchant_products = Product.objects.filter(merchant=instance.merchant)
        Product.objects.exclude(merchant=instance.merchant, retailer_id__in=retailer_ids)
