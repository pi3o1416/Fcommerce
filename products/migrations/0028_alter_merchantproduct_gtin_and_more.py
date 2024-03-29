# Generated by Django 4.2.1 on 2023-07-05 08:25

from django.db import migrations
import products.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_merchantproduct_delete_merchantproducts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantproduct',
            name='gtin',
            field=products.fields.GTINField(blank=True, max_length=50, verbose_name='Global Trade Item Number'),
        ),
        migrations.AlterField(
            model_name='merchantproduct',
            name='retailer_id',
            field=products.fields.RetailerIDField(blank=True, max_length=100, unique=True, verbose_name='Retailer ID'),
        ),
    ]
