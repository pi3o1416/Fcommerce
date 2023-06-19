# Generated by Django 4.2.1 on 2023-06-19 05:59

from django.db import migrations
import products.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_retailer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='gtin',
            field=products.fields.GTINField(editable=False, max_length=50, unique=True, verbose_name='Global Trade Item Number'),
        ),
    ]
