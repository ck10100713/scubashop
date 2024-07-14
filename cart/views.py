from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
from shop.models import Goods

@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, goods_id):
    goods = get_object_or_404(Goods, id=goods_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, goods=goods)
    if not created:
        cart_item.amount += 1
        cart_item.save()
    return redirect('cart:cart_detail')

@login_required
def remove_from_cart(request, goods_id):
    goods = get_object_or_404(Goods, id=goods_id)
    cart_item = Cart.objects.get(user=request.user, goods=goods)
    if cart_item.amount > 1:
        cart_item.amount -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

@login_required
def delete_from_cart(request, goods_id):
    goods = get_object_or_404(Goods, id=goods_id)
    cart_item = Cart.objects.get(user=request.user, goods=goods)
    cart_item.delete()
    return redirect('cart:cart_detail')

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CartSerializer
from rest_framework import permissions
from rest_framework.decorators import permission_classes

@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def cart_list(request, user_id):
    cart_items = Cart.objects.filter(user_id=user_id)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)