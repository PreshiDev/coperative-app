# Generated by Django 2.1.7 on 2019-09-28 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0009_loansissue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanissue',
            name='loan_num',
            field=models.CharField(default='', editable=False, max_length=255, unique=True),
        ),
    ]
