# Generated by Django 4.2.1 on 2023-06-18 09:50

import django.contrib.postgres.fields
from django.db import migrations, models
import django_countries.fields
import products.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('url', models.URLField(verbose_name='Product URL')),
                ('image_url', models.URLField(verbose_name='Image URL')),
                ('currency', models.CharField(choices=[('BDT', 'BDT'), ('USD', 'USD')], max_length=3, verbose_name='Currency')),
                ('price', models.DecimalField(decimal_places=4, max_digits=12, verbose_name='Price')),
                ('retailer_id', models.CharField(max_length=100, verbose_name='Retailer ID')),
                ('gtin', products.fields.GTINField(editable=False, max_length=50, verbose_name='Global Trade Item Number')),
                ('condition', models.CharField(blank=True, choices=[('new', 'New'), ('refurbished', 'Refurbished'), ('used', 'Used'), ('used_like_new', 'Used Like New'), ('used_good', 'Used Good')], max_length=50, null=True, verbose_name='Condition')),
                ('availability', models.CharField(blank=True, choices=[('in stock', 'In Stock'), ('out of stock', 'Out of Stock'), ('preorder', 'Preorder'), ('available for order', 'Available for Order'), ('discontinued', 'Discontinued'), ('pending', 'Pending')], max_length=100, null=True, verbose_name='Availability')),
                ('brand', models.CharField(blank=True, max_length=100, null=True, verbose_name='Brand')),
                ('category', models.CharField(blank=True, max_length=100, null=True, verbose_name='Category')),
                ('color', models.CharField(blank=True, null=True, verbose_name='Color')),
                ('visibility', models.CharField(blank=True, choices=[('staging', 'Staging'), ('published', 'Published')], default='published', max_length=50, null=True, verbose_name='Visibility')),
                ('website_link', models.URLField(blank=True, null=True, verbose_name='Website Link')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='Expiration Date')),
                ('additional_image_urls', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, null=True, size=None, verbose_name='Additional Images')),
                ('additional_variant_attributes', models.JSONField(blank=True, null=True, verbose_name='Additional Varients')),
                ('checkout_url', models.URLField(blank=True, null=True, verbose_name='Checkout URL')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('size', models.CharField(blank=True, null=True, verbose_name='Size')),
                ('short_description', models.TextField(blank=True, null=True, verbose_name='Short Description')),
                ('sale_price', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True, verbose_name='Sale Price')),
                ('sale_price_start_date', models.DateTimeField(blank=True, null=True, verbose_name='Sale Price Start Date')),
                ('sale_price_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Sale Price End Date')),
                ('return_policy_days', models.IntegerField(blank=True, null=True, verbose_name='Return Policy Days')),
                ('product_type', models.CharField(max_length=200, verbose_name='Product Type')),
                ('pattern', models.CharField(blank=True, max_length=100, null=True, verbose_name='Pattern')),
                ('origin_country', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Country')),
                ('offer_price_amount', models.IntegerField(blank=True, null=True, verbose_name='Offer Price')),
                ('offer_price_start_date', models.DateTimeField(blank=True, null=True, verbose_name='Offer Price Start Date')),
                ('offer_price_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Offer Price End Date')),
                ('material', models.CharField(blank=True, max_length=200, null=True, verbose_name='Material')),
                ('inventory', models.IntegerField(blank=True, null=True, verbose_name='Inventory Count')),
                ('importer_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Importer Name')),
                ('importer_address', products.fields.AddressJSONField(blank=True, null=True, verbose_name='Importer Address')),
                ('gender', models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male'), ('unisex', 'Unisex')], max_length=20, null=True, verbose_name='Gender')),
            ],
        ),
    ]
