from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
from shop.models import Product, Category, ProductImage

@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart/detail.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:detail')

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart.objects.get(user=request.user, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:detail')

@login_required
def delete_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart.objects.get(user=request.user, product=product)
    cart_item.delete()
    return redirect('cart:detail')

# api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CartSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user']
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

# @api_view(['GET'])
# def api_overview(request):
#     api_urls = {
#         'Cart List': '/api/cart/<int:user_id>/',
#     }
#     return Response(api_urls)

# @api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# def list_cart(request, user_id):
#     # 根據請求方法設置權限
#     if request.method in ['POST', 'PATCH', 'DELETE']:
#         permission_classes = [IsAdminUser]
#     else:
#         permission_classes = []
#     # 檢查權限
#     if permission_classes:
#         for permission in permission_classes:
#             if not permission().has_permission(request, None):
#                 return Response(status=status.HTTP_403_FORBIDDEN)

#     if request.method == 'GET':
#         cart_items = Cart.objects.filter(user=user_id)
#         if not cart_items:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = CartSerializer(cart_items, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'PATCH':
#         cart_items = Cart.objects.filter(user=user_id)
#         serializer = CartSerializer(cart_items, data=request.data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         cart_items = Cart.objects.filter(user=user_id)
#         cart_items.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# @permission_classes([permissions.IsAdminUser])
# def cart_list(request):
#     cart_items = Cart.objects.all()
#     if not cart_items:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     serializer = CartSerializer(cart_items, many=True)
#     return Response(serializer.data)