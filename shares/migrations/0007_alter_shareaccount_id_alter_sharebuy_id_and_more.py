# Generated by Django 4.2 on 2024-08-19 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0006_auto_20190928_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareaccount',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sharebuy',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sharesell',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
