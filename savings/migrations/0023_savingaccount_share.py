# Generated by Django 5.1.1 on 2024-09-18 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0022_savingaccount_commod_savingaccount_interest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingaccount',
            name='share',
            field=models.PositiveIntegerField(default=0),
        ),
    ]