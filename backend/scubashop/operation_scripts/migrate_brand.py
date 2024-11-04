import os
# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scubashop.settings')
import django
django.setup()
from shop.models import Product, Category, Brand

# 获取所有数据
products = Product.objects.all()
categories = Category.objects.all()
brands = Brand.objects.all()

for product in products:
    if product.brand:
        # 查找或创建品牌
        brand, created = Brand.objects.get_or_create(name=product.brand)
        # 更新产品的品牌
        product.brand = brand
        product.save()
        print(f'产品 {product.name} 的品牌 {brand.name} 已创建')
