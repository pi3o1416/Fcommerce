
import uuid
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

from products.models import MerchantProduct

Merchant = get_user_model()


class Order(models.Model):
    class AcceptedCurrency(models.TextChoices):
        BDT = 'BDT', _('BDT')
        USD = 'USD', _('USD')

    class PaymentStatus(models.IntegerChoices):
        INITIATED = 0, _('Initiated')
        ATTEMPT = 1, _('Attempt')
        SUCCESSFUL = 2, _('Successful')
        CANCELED = 3, _('Cancled')
        CHARGEBACK = 4, _('Chargeback')
        ON_HOLD = 5, _('On-Hold')
        SUSPECT = 6, _('Suspect')
        FAILED = 7, _('Faliled')
        REFUNDED = 8, _('Refunded')
        INCOMPLETE = 9, _('Incomplete')
        REFUND_VOID = 10, _('Refund-Void')
        ERROR_CUSTOMER_PAYMENT = 11, _('Error-Customer-Refund')
        CHARGEBACK_REFUND = 12, _('Chargeback-Refund')
        MISSING_AUTHORISED_EMAIL = 13, _('Missing-Authorised-Email')

    merchant = models.ForeignKey(
        to=Merchant,
        on_delete=models.CASCADE,
        related_name='placed_orders',
        verbose_name=_('Merchant')
    )
    customer_name = models.CharField(
        verbose_name=_('Customer Name'),
        max_length=200
    )
    customer_email = models.EmailField(
        verbose_name=_('Customer Email'),
        max_length=200,
        default='dummy@aamarpay.com'
    )
    customer_phone_no = models.CharField(
        verbose_name=_('Customer Phone No'),
        max_length=100
    )
    payment_currency = models.CharField(
        verbose_name=_('Currency'),
        max_length=3,
        choices=AcceptedCurrency.choices,
        null=True,
        blank=True
    )
    shipping_address = models.CharField(
        max_length=500,
        verbose_name=_('Shipping Address')
    )
    products = models.ManyToManyField(
        to=MerchantProduct,
        related_name='orders',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    description = models.TextField(
        default="FCommerce Payment"
    )
    transaction_id = models.UUIDField(
        verbose_name=_('Transaction ID'),
        default=uuid.uuid4
    )
    payment_status = models.IntegerField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.INITIATED
    )
    pg_transaction_id = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    @property
    def total_amount(self):
        total_amount = 0
        for product in self.products.all():
            if product.sale_price is not None:
                total_amount += product.sale_price
            else:
                total_amount += product.price
        return total_amount
