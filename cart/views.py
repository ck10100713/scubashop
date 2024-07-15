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
from rest_framework import status

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/api/<int:user_id>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def list_cart(request, user_id):
    if user_id == request.user or request.user.is_staff:
        cart_items = Cart.objects.filter(user=user_id)
        if not cart_items:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def cart_list(request):
    cart_items = Cart.objects.all()
    if not cart_items:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)