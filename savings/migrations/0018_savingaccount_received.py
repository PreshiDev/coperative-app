# Generated by Django 4.0.4 on 2024-08-31 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0017_remove_savingaccount_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingaccount',
            name='received',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
