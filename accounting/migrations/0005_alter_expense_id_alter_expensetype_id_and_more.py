# Generated by Django 4.2 on 2024-08-19 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_auto_20200526_0510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='expensetype',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='income',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='incometype',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
