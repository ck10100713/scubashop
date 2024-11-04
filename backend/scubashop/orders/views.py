from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Order, OrderItem
from account_center.models import DefaultRecipient, UserProfile
from cart.models import Cart
from .serializers import OrderSerializer, OrderItemSerializer
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
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

class OrderCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.get_total_price() for item in cart_items)
        if total_price == 0:
            return Response({'error': '您的購物車內沒有商品'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'cart_items': OrderItemSerializer(cart_items, many=True).data, 'total_price': total_price}, status=status.HTTP_200_OK)

class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @never_cache
    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({'error': '您的購物車內沒有商品'}, status=status.HTTP_400_BAD_REQUEST)
        total_price = sum(item.get_total_price() for item in cart_items)
        try:
            default_recipient = DefaultRecipient.objects.get(user=request.user)
        except DefaultRecipient.DoesNotExist:
            default_recipient = None
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

        form_data = request.data
        name = form_data.get('recipient_name')
        address = form_data.get('recipient_address')
        contact_number = form_data.get('recipient_number')
        email = form_data.get('email')
        credit_card = form_data.get('credit_card')
        amount = total_price

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
                quantity=item.quantity
            )
        cart_items.delete()
        return Response({'message': '訂單創建成功', 'order_id': order.id}, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if order.user == request.user or request.user.is_staff:
            total_cost = sum(item.get_total_price() for item in order.items.all())
            return Response({'order': OrderSerializer(order).data, 'total_cost': total_cost}, status=status.HTTP_200_OK)
        return Response({'error': '無權查看此訂單'}, status=status.HTTP_403_FORBIDDEN)

class OrderHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return Response({'orders': OrderSerializer(orders, many=True).data}, status=status.HTTP_200_OK)