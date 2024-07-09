from rest_framework import serializers
from .models import User, GoodsType, Goods, CartInfo

class GoodsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsType
        fields = '__all__'

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'

class CartInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartInfo
        fields = '__all__'

from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','username', 'password', 'email')  # 選擇字段
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # 確保密碼是哈希過的
        return user

def register_user(data):
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return {
            "success": True,
            "data": serializer.data,
            "message": "註冊成功"
        }
    else:
        return {
            "success": False,
            "errors": serializer.errors,
            "message": "註冊失敗"
        }