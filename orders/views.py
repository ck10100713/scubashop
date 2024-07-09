# order/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import Cart

@login_required
def order_create(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                goods=item.goods,
                price=item.goods.price,
                quantity=item.amount
            )
        cart_items.delete()  # 清空购物车
        print(f'Order {order.id} created')
        return redirect('orders:order_detail', order_id=order.id)
    return render(request, 'orders/order_create.html',  {'cart_items': cart_items, 'total_price': total_price})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_cost = sum(item.get_total_price() for item in order.items.all())
    return render(request, 'orders/order_detail.html', {'order': order, 'total_cost': total_cost})
