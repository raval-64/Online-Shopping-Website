# Generated by Django 2.2.5 on 2019-10-02 17:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=60)),
                ('product_price', models.FloatField()),
                ('product_desc', models.TextField()),
                ('product_quantity', models.IntegerField(validators=[django.core.validators.RegexValidator('^\\d[0-9]*$')])),
                ('product_brand', models.CharField(max_length=15)),
                ('product_add_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='product_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_category_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='product_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type_name', models.CharField(max_length=20)),
                ('product_category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product_category')),
            ],
        ),
        migrations.CreateModel(
            name='product_gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery_name', models.FileField(upload_to='')),
                ('gallery_type', models.CharField(max_length=10)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product_type'),
        ),
        migrations.AddField(
            model_name='product',
            name='seller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.seller_info'),
        ),
    ]
