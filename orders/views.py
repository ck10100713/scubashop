# order/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from account_center.models import DefaultRecipient, UserProfile
from cart.models import Cart
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import OrderSerializer, OrderItemSerializer

@login_required
def order_check(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    if total_price == 0:
        messages.warning(request, '您的購物車內沒有商品')
        return redirect('cart:detail')
    if request.method == 'POST':
        return redirect('orders:create')
    return render(request, 'orders/check.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def order_create(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    try:
        default_recipient = DefaultRecipient.objects.get(user=request.user)
    except DefaultRecipient.DoesNotExist:
        default_recipient = None
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form_data = request.POST
        name = form_data.get('recipient_name')
        address = form_data.get('recipient_address')
        contact_number = form_data.get('recipient_number')
        email = form_data.get('email')
        credit_card = form_data.get('credit_card')
        amount=total_price
        # 創建訂單
        order = Order.objects.create(
            user=request.user,
            name=name,
            address=address,
            contact_number=contact_number,
            email=email,
            amount=amount,
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.amount
            )
        # 清空購物車
        cart_items.delete()
        # 跳轉到支付頁面
        return redirect('payment:process', order_id=order.id)

    return render(request, 'orders/create.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'default_recipient': default_recipient,
        'user_profile': user_profile
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_cost = sum(item.get_total_price() for item in order.items.all())
    if order.user == request.user or request.user.is_staff:
        total_cost = sum(item.get_total_price() for item in order.items.all())
        return render(request, 'orders/detail.html', {'order': order, 'total_cost': total_cost})
    else:
        # 如果用戶沒有權限查看訂單，返回403禁止訪問
        return render(request, '403.html')  # 確保有一個403.html模板文件

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})

from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderFilter

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderFilter
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

# @api_view(['GET'])
# def api_overview(request):
#     api_urls = {
#         'Order List': 'api/orderbooks/',
#         'Order Detail': 'api/orderbooks/<str:pk>/',
#     }
#     return Response(api_urls)

# @api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
# @permission_classes([permissions.IsAdminUser])
# def orderbooks(request, pk=None):
#     if request.method == 'GET':
#         if pk:
#             order = Order.objects.get(id=pk)
#             serializer = OrderSerializer(order, many=False)
#         else:
#             # get all orders which content only user id and order id
#             orders = Order.objects.all()
#             serializer = OrderSummarySerializer(orders, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'PUT':
#         order = Order.objects.get(id=pk)
#         serializer = OrderSerializer(instance=order, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         order = Order.objects.get(id=pk)
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     elif request.method == 'PATCH':
#         order = Order.objects.get(id=pk)
#         serializer = OrderSerializer(instance=order, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)