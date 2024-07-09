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

# @login_required
# def clear_cart(request):
#     Cart.objects.filter(user=request.user).delete()
#     return redirect('cart:cart_detail')

# @login_required
# def update_cart(request, goods_id):
#     goods = get_object_or_404(Goods, id=goods_id)
#     cart_item = Cart.objects.get(user=request.user, goods=goods)
#     cart_item.amount = int(request.POST['amount'])
#     cart_item.save()
#     return redirect('cart:cart_detail')