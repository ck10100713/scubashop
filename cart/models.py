# cart/models.py
from django.db import models
from django.contrib.auth.models import User
from shop.models import Goods

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.goods.price * self.amount

    class Meta:
        unique_together = ('user', 'goods')