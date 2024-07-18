from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Goods, GoodsType
from .models import Product, Category, ProductImage
from django.contrib.auth.forms import UserCreationForm
from .forms import ProductForm, CategoryForm
from rest_framework.decorators import permission_classes
from rest_framework import permissions

def index_views(request):
    products = Product.objects.filter(isActive=True).order_by('-id')[:3]
    context = {
        'products': products
    }
    return render(request, 'index.html', context)

def shop_views(request):
    categories = Category.objects.all()
    products = Product.objects.filter(isActive=True)
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(categories__id=category_id)
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/shop.html', context)

def photo_views(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop/photo.html', context)

# @permission_classes([permissions.IsAdminUser])
# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('create_product')   # 假设你有一个 product_list 的 URL 名称
#     else:
#         form = ProductForm()
#     return render(request, 'shop/create_product.html', {'form': form})

# @permission_classes([permissions.IsAdminUser])
# def create_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('create_category')   # 假设你有一个 category_list 的 URL 名称
#     else:
#         form = CategoryForm()
#     return render(request, 'shop/category_form.html', {'form': form})

def product_detail_views(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'shop/detail.html', context)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import GoodsSerializer, GoodsTypeSerializer
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Goods': 'api/goods',
        'Goods Detail': 'api/goods/<str:pk>',
        'Goods Type': 'api/goodstype',
        'Goods Type Detail': 'api/goodstype/<str:pk>',
    }
    return Response(api_urls)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def goods(request, pk=None):
    # 根據請求方法設置權限
    if request.method in ['POST', 'PATCH', 'DELETE']:
        permission_classes = [IsAdminUser]
    else:
        permission_classes = []

    # 檢查權限
    for permission in permission_classes:
        if not permission().has_permission(request, view=goods):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if pk:
            goods = Goods.objects.get(id=pk)
            serializer = GoodsSerializer(goods, many=False)
        else:
            goods = Goods.objects.all()
            serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        goods = Goods.objects.get(id=pk)
        serializer = GoodsSerializer(instance=goods, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        goods = Goods.objects.get(id=pk)
        goods.delete()
        return Response('Item deleted', status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def goodstype(request, pk=None):
    # 根據請求方法設置權限
    if request.method in ['POST', 'PATCH', 'DELETE']:
        permission_classes = [IsAdminUser]
    else:
        permission_classes = []
    # 檢查權限
    for permission in permission_classes:
        if not permission().has_permission(request, view=goodstype):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if pk:
            goodstype = GoodsType.objects.get(id=pk)
            serializer = GoodsTypeSerializer(goodstype, many=False)
        else:
            goodstype = GoodsType.objects.all()
            serializer = GoodsTypeSerializer(goodstype, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GoodsTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        goodstype = GoodsType.objects.get(id=pk)
        serializer = GoodsTypeSerializer(instance=goodstype, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        goodstype = GoodsType.objects.get(id=pk)
        goodstype.delete()
        return Response('Item deleted', status=status.HTTP_204_NO_CONTENT)