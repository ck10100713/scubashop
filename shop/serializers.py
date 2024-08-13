from rest_framework import serializers
from .models import Product, Category
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']

# class ProductListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name']
#         read_only_fields = ['id']