# Generated by Django 4.2.1 on 2023-06-18 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_product_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='checkout_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='importer_address',
        ),
        migrations.RemoveField(
            model_name='product',
            name='website_link',
        ),
    ]