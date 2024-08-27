import os
import csv
from django.core.files import File
from django.core.files.images import ImageFile
from django.conf import settings

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scubashop.settings')
import django
django.setup()

from shop.models import Product, Category, Brand
from uuid import uuid4

def product_image_upload_to(instance, filename):
    category_name = instance.categories.name
    brand_name = instance.brand.name
    product_name = instance.name
    ext = 'jpg'
    filename = f'{uuid4().hex}.{ext}'
    return os.path.join('products', category_name, brand_name, product_name, filename)

def get_product_image_path(instance, filename):
    base_directory = '/Users/guobaichen/Desktop/商品'
    category_name = instance.categories.name
    brand_name = instance.brand.name
    product_name = instance.name
    ext = 'jpg'
    filename = product_name.replace(' ', '-').replace('/', '-') + f'.{ext}'
    return os.path.join(base_directory, category_name, brand_name, product_name, filename)

import boto3

s3 = boto3.client('s3')
bucket_name = 'scubashopbucket'
media_root = 'products'

products = Product.objects.all()
for product in products:
    if product.image:
        old_image = product.image
        image_path = get_product_image_path(product, old_image.name)
        new_name = product_image_upload_to(product, old_image.name)
        product.image.name = new_name
        product.save()
        s3.upload_file(image_path, bucket_name, f'media/{new_name}')
        print(f'{image_path} uploaded to S3')
        print(f'{new_name} uploaded to S3')