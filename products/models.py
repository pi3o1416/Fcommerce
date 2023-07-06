
from django.db import models
from django.db import transaction
from django.db.models import Q, CheckConstraint
from django_countries.fields import CountryField
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from services.querysets import TemplateQuerySet
from facebook_integration.exceptions import FacebookIntegrationIsNotComplete
from facebook_integration.utils import FacebookAdapter
from facebook_integration.models import FacebookIntegrationData
from .fields import GTINField, RetailerIDField


Merchant = get_user_model()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(model=self.model, using=self._db)

    @transaction.atomic
    def sync_merchant_products_with_facebook(self, merchant):
        # TODO: Divide this method to multiple method
        try:
            facebook_adapter = FacebookAdapter.merchant_facebook_adapter(merchant=merchant)
            merchant_inventory = self.filter(merchant=merchant)
            facebook_products_data = facebook_adapter.get_catalog_items()
            if facebook_products_data is not None:
                facebook_products = [self.model(**product_data, merchant=merchant) for product_data in facebook_products_data]
                inventory_products = self.model.objects.filter(id__in=merchant_inventory)
                products_absent_on_facebook = set(inventory_products) - set(facebook_products)
                products_absent_on_inventory = set(facebook_products) - set(inventory_products)
                self.bulk_create(products_absent_on_inventory)
                added_products_fb_id = facebook_adapter.bulk_add_catalog_item(products=products_absent_on_facebook)
                if added_products_fb_id is not None:
                    for merchant_product in products_absent_on_facebook:
                        merchant_product.facebook_id = added_products_fb_id[merchant_product.id]['facebook_id']
                        self.bulk_update(products_absent_on_facebook, ['facebook_id'])
            return True
        except FacebookIntegrationData.DoesNotExist:
            raise FacebookIntegrationIsNotComplete('Facebook Integration Not Completed Yet')

    def filter_from_query_params(self, request):
        return self.get_queryset().filter_from_query_params(request=request)

    def filter_from_related_query_params(self, request, related_fields):
        return self.get_queryset().filter_with_related_fields(request=request, related_fields=related_fields)

    def merchant_products(self, merchant):
        return self.get_queryset().merchant_products(merchant=merchant)


class ProductQuerySet(TemplateQuerySet):
    def merchant_products(self, merchant):
        return self.filter(merchant=merchant)


class MerchantProduct(models.Model):
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

    merchant = models.ForeignKey(
        to=Merchant,
        on_delete=models.CASCADE,
        related_name='inventory'
    )
    name = models.CharField(
        verbose_name=_('Title'),
        max_length=500
    )
    description = models.TextField(
        verbose_name=_('Description')
    )
    url = models.URLField(
        verbose_name=_('Product URL'),
        max_length=500
    )
    image_url = models.URLField(
        verbose_name=_('Image URL'),
        max_length=500
    )
    currency = models.CharField(
        verbose_name=_('Currency'),
        max_length=3,
        choices=AcceptedCurrency.choices
    )
    price = models.DecimalField(
        verbose_name=_('Price'),
        max_digits=16,
        decimal_places=2
    )
    retailer_id = RetailerIDField(
        verbose_name=_('Retailer ID'),
        max_length=100,
        unique=True
    )
    gtin = GTINField(
        verbose_name=_('Global Trade Item Number'),
        max_length=50,
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
        blank=True,
    )
    additional_image_urls = ArrayField(
        verbose_name=_('Additional Images'),
        base_field=models.URLField(max_length=500),
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
        max_digits=16,
        decimal_places=2,
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
    facebook_id = models.CharField(
        verbose_name=_('Facebook ID'),
        max_length=100,
        null=True,
        blank=True
    )
    objects = ProductManager()

    class Meta:
        unique_together = (('merchant', 'retailer_id'))
        constraints = [
            CheckConstraint(
                check=Q(expiration_date__gt=timezone.now().date()),
                name='expiration_date_greater_than_today'
            ),
            CheckConstraint(
                check=Q(price__gt=0),
                name='Price should be greater than 0'
            )
        ]

    def __str__(self):
        return self.name

    def __eq__(self, merchant_product: 'MerchantProduct'):
        if self.pk is not None and merchant_product.pk is not None:
            if self.merchant_id == merchant_product.merchant_id and hash(self.retailer_id) == hash(merchant_product.retailer_id):
                return True
        else:
            if hash(self.retailer_id) == hash(merchant_product.retailer_id):
                return True
        return False

    def __hash__(self):
        return hash(self.retailer_id)
