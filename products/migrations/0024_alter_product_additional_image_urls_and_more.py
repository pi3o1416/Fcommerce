# Generated by Django 4.2.1 on 2023-07-04 12:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_remove_product_expiration_date_greater_than_today_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='additional_image_urls',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=500), blank=True, null=True, size=None, verbose_name='Additional Images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.URLField(max_length=500, verbose_name='Image URL'),
        ),
        migrations.AlterField(
            model_name='product',
            name='importer_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Importer Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='material',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Material'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Product Type'),
        ),
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(max_length=500, verbose_name='Product URL'),
        ),
    ]
