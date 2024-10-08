# Generated by Django 4.0.4 on 2024-08-31 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('savings', '0018_savingaccount_received'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savingaccount',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving_accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]
