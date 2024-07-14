from rest_framework import serializers
from .models import Goods, GoodsType

class GoodsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsType
        fields = '__all__'
        read_only_fields = ['id']

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
        read_only_fields = ['id']