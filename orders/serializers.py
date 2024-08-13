from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'paid', 'items']

# class OrderSummarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         # display toptal amount of order
#         fields = ['id', 'name', 'user', 'amount']