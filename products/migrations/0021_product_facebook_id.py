# Generated by Django 4.2.1 on 2023-06-26 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_remove_product_return_policy_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='facebook_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Facebook ID'),
        ),
    ]
