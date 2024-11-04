# cart/models.py
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product, Category, ProductImage

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ('user', 'product')