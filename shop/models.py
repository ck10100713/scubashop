from django.db import models
import os
from uuid import uuid4

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

def product_image_upload_to(instance, filename):
    category_name = instance.categories.name
    brand_name = instance.brand
    product_name = instance.name
    ext = filename.split('.')[-1]
    filename = f'{uuid4().hex}.{ext}'
    return os.path.join('products', category_name, brand_name, product_name, filename)

class Product(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=255)
    image = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    # image = models.ImageField(upload_to='', blank=True, null=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/product/{self.id}/'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_upload_to)

    def __str__(self):
        return f'{self.product.name} 圖片'