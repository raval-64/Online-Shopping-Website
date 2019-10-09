# Generated by Django 2.0.4 on 2018-05-24 04:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osm', '0007_auto_20180524_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_info',
            name='order_quantity',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator('^\\d[0-9]*$')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_quantity',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator('^\\d[0-9]*$')]),
        ),
    ]
