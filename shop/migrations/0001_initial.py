# Generated by Django 5.0.6 on 2024-07-18 05:52

import django.db.models.deletion
import shop.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='類型標題')),
                ('picture', models.ImageField(null=True, upload_to='upload/goodstype', verbose_name='類型圖片')),
                ('desc', models.TextField(verbose_name='類型描述')),
            ],
            options={
                'verbose_name': '商品類型',
                'verbose_name_plural': '商品類型',
                'db_table': 'goods_type',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='商品名稱')),
                ('price', models.DecimalField(decimal_places=0, max_digits=7, verbose_name='商品價格')),
                ('spec', models.CharField(max_length=20, verbose_name='商品規格')),
                ('picture', models.ImageField(null=True, upload_to='upload/goods', verbose_name='商品圖片')),
                ('isActive', models.BooleanField(default=True, verbose_name='是否上架')),
                ('goodsType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.goodstype', verbose_name='商品類型')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'db_table': 'goods',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('description', models.TextField()),
                ('size', models.CharField(blank=True, max_length=50, null=True)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('brand', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to=shop.models.product_image_upload_to)),
                ('isActive', models.BooleanField(default=True)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=shop.models.product_image_upload_to)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product')),
            ],
        ),
    ]
