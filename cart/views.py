from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Cart
from shop.models import Product
from .serializers import CartSerializer

@method_decorator(login_required, name='dispatch')
class CartDetailView(APIView):
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.get_total_price() for item in cart_items)
        serializer = CartSerializer(cart_items, many=True)
        return Response({'cart_items': serializer.data, 'total_price': total_price}, status=status.HTTP_200_OK)

@method_decorator(login_required, name='dispatch')
class AddToCartView(APIView):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(APIView):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart_item = Cart.objects.get(user=request.user, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)