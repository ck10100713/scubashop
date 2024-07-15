from django.db import models

# Create your models here.

#商品類型
class GoodsType(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name='類型標題')
    picture = models.ImageField(
        upload_to='upload/goodstype',
        null=True,
        verbose_name="類型圖片")
    desc = models.TextField(verbose_name='類型描述')

    def __str__(self):
        return self.title

    def to_dict(self):
        dic = {
        'title':self.title,
        'picture':self.picture.__str__(),
        'desc':self.desc,
        }
        return dic

    class Meta:
        db_table = "goods_type"
        verbose_name = "商品類型"
        verbose_name_plural = verbose_name

#商品
class Goods(models.Model):
    title = models.CharField(
        max_length=40,
        verbose_name='商品名稱'
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        verbose_name='商品價格'
    )
    spec = models.CharField(
        max_length=20,
        verbose_name='商品規格'
    )
    picture = models.ImageField(
        upload_to='upload/goods',
        null=True,
        verbose_name='商品圖片'
    )
    goodsType = models.ForeignKey(
        GoodsType,
        verbose_name='商品類型',
        on_delete=models.CASCADE
    )
    isActive = models.BooleanField(
        default = True,
        verbose_name='是否上架'
    )
    def to_dict(self):
        dic = {
        'title':self.title,
        'picture':self.picture.__str__(),
        'price':self.price,
        }
        return dic
    def __str__(self):
        return self.title

    def get_title(self):
        return self.title

    def get_price(self):
        return self.price.__str__()

    def get_picture(self):
        return self.picture.__str__()

    def get_absolute_url(self):
        return '/product/{}/'.format(self.id)

    class Meta:
        db_table = "goods"
        verbose_name = "商品"
        verbose_name_plural = verbose_name