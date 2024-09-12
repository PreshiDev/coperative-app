# Generated by Django 2.1.7 on 2019-06-05 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='delete_status',
            field=models.CharField(choices=[('False', 'False'), ('True', 'True')], default='False', editable=False, max_length=5),
        ),
        migrations.AddField(
            model_name='income',
            name='delete_status',
            field=models.CharField(choices=[('False', 'False'), ('True', 'True')], default='False', editable=False, max_length=5),
        ),
    ]
