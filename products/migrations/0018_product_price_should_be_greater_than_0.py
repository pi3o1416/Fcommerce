# Generated by Django 4.2.1 on 2023-06-22 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_product_retailer_id'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(('price__gt', 0)), name='Price should be greater than 0'),
        ),
    ]
