# Generated by Django 4.2.1 on 2023-06-19 11:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_product_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateField(blank=True, null=True, verbose_name='Expiration Date'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(('expiration_date__gt', datetime.date(2023, 6, 19))), name='expiration_date_greater_than_today'),
        ),
    ]