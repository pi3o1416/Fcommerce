# Generated by Django 4.2.1 on 2023-06-18 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Product Type'),
        ),
    ]