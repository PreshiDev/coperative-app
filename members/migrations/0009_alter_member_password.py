# Generated by Django 4.2 on 2024-08-19 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_member_image_member_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
