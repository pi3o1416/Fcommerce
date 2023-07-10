
from django.contrib.auth import get_user_model
from celery import shared_task
from .models import MerchantProduct


Merchant = get_user_model()


@shared_task(name='sync_inventory_with_facebook')
def sync_inventory_with_facebook(merchant_id):
    merchant = Merchant.objects.get(id=merchant_id)
    MerchantProduct.objects.sync_merchant_products_with_facebook(merchant=merchant)


@shared_task(name='add_product_on_facebook')
def add_product_on_facebook(product_id):
    merchant_product = MerchantProduct.objects.get(id=product_id)
    merchant_product.add_on_facebook()


@shared_task(name='update_product_on_facebook')
def update_product_on_facebook(product_id):
    merchant_product = MerchantProduct.objects.get(id=product_id)
    merchant_product.update_on_facebook()


@shared_task(name='delete_product_on_facebook')
def delete_product(product_id):
    merchant_product = MerchantProduct.objects.get(id=product_id)
    merchant_product.delete()
