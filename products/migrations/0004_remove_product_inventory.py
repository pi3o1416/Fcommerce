# Generated by Django 4.2.1 on 2023-06-18 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_checkout_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='inventory',
        ),
    ]
