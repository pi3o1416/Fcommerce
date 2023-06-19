# Generated by Django 4.2.1 on 2023-06-19 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_merchantproducts_merchant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(blank=True, choices=[('new', 'New'), ('refurbished', 'Refurbished'), ('used', 'Used'), ('used_like_new', 'Used Like New'), ('used_good', 'Used Good'), ('used_fair', 'Used Fair'), ('cpo', 'CPO'), ('open_box_new', 'Open Box New')], max_length=50, null=True, verbose_name='Condition'),
        ),
    ]