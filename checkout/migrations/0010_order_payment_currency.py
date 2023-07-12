# Generated by Django 4.2.1 on 2023-07-11 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_alter_order_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_currency',
            field=models.CharField(choices=[('BDT', 'BDT'), ('USD', 'USD')], default='BDT', max_length=3, verbose_name='Currency'),
            preserve_default=False,
        ),
    ]