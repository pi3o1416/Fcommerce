
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Merchant


@receiver(signal=pre_save, sender=Merchant)
def encode_password_before_save(sender, instance: Merchant, **kwargs):
    if 'password' in instance.get_dirty_fields():
        instance.set_password(instance.password)
