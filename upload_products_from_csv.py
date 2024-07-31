import os
import csv
from django.core.files import File
from django.core.files.images import ImageFile
from django.conf import settings


# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scubashop.settings')
import django
django.setup()
from shop.models import Product
from shop.models import Category

# 定义 CSV 文件路径
csv_file_path = '/Users/guobaichen/Documents/MyProgram/products.csv'

# 读取 CSV 文件并上传数据
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        product_name = row['商品名稱']
        category_name = row['商品種類']
        product_categories, created = Category.objects.get_or_create(name=category_name)
        product_brand = row['商品品牌']
        product_image_path = row['商品圖片位置']
        product_price = row['商品金額']
        product_description = row.get('商品介紹', '')
        product_size = row.get('商品規格大小', '')
        product_color = row.get('商品規格顏色', '')
        # 获取图片路径并打开文件
        image_path = os.path.join(settings.MEDIA_ROOT, product_image_path)
        with open(image_path, 'rb') as image_file:
            image = ImageFile(image_file, name=os.path.basename(image_path))

            # # 创建并保存商品
            product = Product(
                name=product_name,
                categories=product_categories,
                brand=product_brand,
                price=product_price,
                description=product_description,
                size=product_size,
                color=product_color,
                isActive=True
            )
            product.image.save(os.path.basename(image_path), image)
            product.save()

print('商品上传完成')
