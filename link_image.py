import os
from django.core.files import File
from django.core.files.images import ImageFile
from django.conf import settings

import boto3
from uuid import uuid4
import slugify

s3 = boto3.client('s3')
bucket_name = 'scubashopbucket'
base_dir = '/Users/guobaichen/Desktop/商品'

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scubashop.settings')
import django
django.setup()

from shop.models import Product, Category, Brand, ProductImage

def product_image_upload_to(instance):
    category_name = slugify.slugify(instance.categories.name)
    brand_name = slugify.slugify(instance.brand.name)
    product_name = slugify.slugify(instance.name)
    ext = 'jpg'
    filename = f'{uuid4().hex}.{ext}'
    return os.path.join('media', 'products', category_name, brand_name, product_name, filename)

def get_picture_path(instance):
    category_name = instance.categories.name
    brand_name = instance.brand.name
    product_name = instance.name
    ext = 'jpg'
    filename = product_name.replace(' ', '-').replace('/', '-')+'.'+ext
    return os.path.join(category_name, brand_name, product_name, filename)

products = Product.objects.all()
for product in products:
    if product.image:
        file_path = product_image_upload_to(product)
        print('file_path = ' + file_path)
        picture_path = os.path.join(base_dir, get_picture_path(product))
        print('picture_path = ' + picture_path)
        save_path = file_path
        print('save_path = ' + save_path)
        product_image, created = ProductImage.objects.get_or_create(product=product)
        product_image.image = file_path
        product_image.save()
        if created:
            print(f'Created new ProductImage for product {product.name} with path {file_path}')
        else:
            print(f'Updated ProductImage for product {product.name} with new path {file_path}')
        s3.upload_file(picture_path, bucket_name, save_path)
        print(f'{picture_path} uploaded to S3')