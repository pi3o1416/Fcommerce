
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.db import models

from .fields import GTINField


class Product(models.Model):
    class AcceptedCurrency(models.TextChoices):
        BDT = 'BDT', _('BDT')
        USD = 'USD', _('USD')

    class ConditionChoices(models.TextChoices):
        NEW = 'new', _('New')
        REFURB = 'refurbished', _('Refurbished')
        USED = 'used', _('Used'),
        USED_LIKE_NEW = 'used_like_new', _('Used Like New')
        USED_GOOD = 'used_good', _('Used Good')
        USED_FAIR = 'used_fair', _('Used Fair')
        CPO = 'cpo', _('CPO')
        OPEN_BOX_NEW = 'open_box_new', _('Open Box New')

    class AvailabilityChoices(models.TextChoices):
        IN_STOCK = 'in stock', _('In Stock')
        OUT_OF_STOCK = 'out of stock', _('Out of Stock')
        PREORDER = 'preorder', _('Preorder')
        AVAILABLE_FOR_ORDER = 'available for order', _('Available for Order')
        DISCONTINUED = 'discontinued', _('Discontinued')
        PENDING = 'pending', _('Pending')

    class VisibilityChoices(models.TextChoices):
        STAGING = 'staging', _('Staging')
        PUBLISHED = 'published', _('Published')

    class GenderChoices(models.TextChoices):
        FEMALE = 'female', _('Female')
        MALE = 'male', _('Male')
        UNISEX = 'unisex', _('Unisex')

    name = models.CharField(
        verbose_name=_('Title'),
        max_length=500
    )
    description = models.TextField(
        verbose_name=_('Description')
    )
    url = models.URLField(
        verbose_name=_('Product URL')
    )
    image_url = models.URLField(
        verbose_name=_('Image URL')
    )
    currency = models.CharField(
        verbose_name=_('Currency'),
        max_length=3,
        choices=AcceptedCurrency.choices
    )
    price = models.DecimalField(
        verbose_name=_('Price'),
        max_digits=12,
        decimal_places=4
    )
    retailer_id = models.CharField(
        verbose_name=_('Content ID'),
        max_length=100,
        unique=True
    )
    gtin = GTINField(
        verbose_name=_('Global Trade Item Number'),
        max_length=50,
        unique=True
    )
    condition = models.CharField(
        verbose_name=_('Condition'),
        max_length=50,
        choices=ConditionChoices.choices,
        null=True,
        blank=True
    )
    availability = models.CharField(
        verbose_name=_('Availability'),
        max_length=100,
        choices=AvailabilityChoices.choices,
        null=True,
        blank=True
    )
    brand = models.CharField(
        verbose_name=_('Brand'),
        max_length=100,
        null=True,
        blank=True
    )
    category = models.CharField(
        verbose_name=_('Product Category'),
        max_length=100,
        null=True,
        blank=True
    )
    color = models.CharField(
        verbose_name=_('Color'),
        null=True,
        blank=True
    )
    visibility = models.CharField(
        verbose_name=_('Visibility'),
        max_length=50,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLISHED,
        null=True,
        blank=True
    )
    expiration_date = models.DateField(
        verbose_name=_('Expiration Date'),
        null=True,
        blank=True
    )
    additional_image_urls = ArrayField(
        verbose_name=_('Additional Images'),
        base_field=models.URLField(),
        null=True,
        blank=True
    )
    additional_variant_attributes = models.JSONField(
        verbose_name=_('Additional Varients'),
        null=True,
        blank=True
    )
    start_date = models.DateField(
        verbose_name=_('Start Date'),
        blank=True,
        null=True
    )
    size = models.CharField(
        verbose_name=_('Size'),
        blank=True,
        null=True
    )
    short_description = models.TextField(
        verbose_name=_('Short Description'),
        null=True,
        blank=True
    )
    sale_price = models.DecimalField(
        verbose_name=_('Sale Price'),
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True
    )
    sale_price_start_date = models.DateTimeField(
        verbose_name='Sale Price Start Date',
        null=True,
        blank=True
    )
    sale_price_end_date = models.DateTimeField(
        verbose_name=_('Sale Price End Date'),
        null=True,
        blank=True
    )
    return_policy_days = models.IntegerField(
        verbose_name=_('Return Policy Days'),
        null=True,
        blank=True
    )
    product_type = models.CharField(
        verbose_name=_('Product Type'),
        max_length=200,
        null=True,
        blank=True
    )
    pattern = models.CharField(
        verbose_name=_('Pattern'),
        max_length=100,
        blank=True,
        null=True
    )
    origin_country = CountryField(
        verbose_name=_('Country'),
        null=True,
        blank=True
    )
    material = models.CharField(
        verbose_name=_('Material'),
        max_length=200,
        null=True,
        blank=True
    )
    importer_name = models.CharField(
        verbose_name=_('Importer Name'),
        max_length=200,
        null=True,
        blank=True
    )
    gender = models.CharField(
        verbose_name=_('Gender'),
        max_length=20,
        choices=GenderChoices.choices,
        null=True,
        blank=True
    )


class MerchantManager(models.Manager):
    pass


class MerchantProducts(models.Model):
    product = models.OneToOneField(
        verbose_name=_('Product'),
        to=Product,
        related_name='product_owner',
        on_delete=models.CASCADE,
        primary_key=True
    )
    merchant = models.ForeignKey(
        verbose_name=_('Merchant'),
        to=get_user_model(),
        related_name='owned_products',
        on_delete=models.RESTRICT,
    )
    objects = MerchantManager()
