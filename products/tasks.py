
from django.contrib.auth import get_user_model
from celery import shared_task
from .models import MerchantProduct


Merchant = get_user_model()


@shared_task(name='sync_inventory_with_facebook')
def sync_inventory_with_facebook(merchant_id):
    merchant = Merchant.objects.get(id=merchant_id)
    MerchantProduct.objects.sync_merchant_products_with_facebook(merchant=merchant)
