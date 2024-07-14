# order/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import Cart

@login_required
def order_check(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    if total_price == 0:
        return redirect('cart:cart_detail')
    if request.method == 'POST':
        return redirect('orders:order_create')
    return render(request, 'orders/order_check.html', {'cart_items': cart_items, 'total_price': total_price})

# @login_required
# def order_create(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     total_price = sum(item.get_total_price() for item in cart_items)
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         contact_number = request.POST.get('contact_number')
#         email = request.POST.get('email')
#         credit_card = request.POST.get('credit_card')


#     return render(request, 'orders/order_create.html', {'cart_items': cart_items, 'total_price': total_price})

# @login_required
# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_create(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        form_data = request.POST  # 获取POST请求的数据

        # 提取表单数据
        name = form_data.get('name')
        address = form_data.get('address')
        contact_number = form_data.get('contact_number')
        email = form_data.get('email')
        credit_card = form_data.get('credit_card')
        # total_price = sum(item.get_total_price() for item in cart_items)

        # 创建订单
        order = Order.objects.create(
            user=request.user,
            name=name,
            address=address,
            contact_number=contact_number,
            email=email,
            credit_card=credit_card,
            # total_price=total_price
        )
        # 将购物车中的商品添加到订单项中
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                goods=item.goods,
                price=item.goods.price,
                quantity=item.amount
            )
        # 清空购物车
        cart_items.delete()
        # 重定向到订单详情页面
        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/order_create.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    total_cost = sum(item.get_total_price() for item in order.items.all())
    return render(request, 'orders/order_detail.html', {'order': order, 'total_cost': total_cost})

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def order_list_create(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([permissions.IsAuthenticated])
# def order_detail(request, pk):
#     order = get_object_or_404(Order, pk=pk, user=request.user)

#     if request.method == 'GET':
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         serializer = OrderSerializer(order, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def order_item_list_create(request):
    if request.method == 'GET':
        items = OrderItem.objects.filter(order__user=request.user)
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            order = get_object_or_404(Order, id=request.data['order'], user=request.user)
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def order_item_detail(request, pk):
    item = get_object_or_404(OrderItem, pk=pk, order__user=request.user)

    if request.method == 'GET':
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = OrderItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)