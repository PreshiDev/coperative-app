# Generated by Django 4.0.4 on 2024-08-31 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0016_savingaccount_received'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savingaccount',
            name='received',
        ),
    ]