# Generated by Django 4.2.1 on 2023-06-22 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facebook_integration', '0002_alter_facebookintegrationdata_access_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookintegrationdata',
            name='merchant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='facebook_info', to=settings.AUTH_USER_MODEL, verbose_name='Merchant'),
        ),
    ]