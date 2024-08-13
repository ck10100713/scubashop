from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
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

def product_detail_views(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'shop/detail.html', context)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProductSerializer, ProductListSerializer
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Products': 'api/products',
        'Products Detail': 'api/products/<str:pk>',
    }
    return Response(api_urls)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def products(request, pk=None):
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
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product, many=False)
        else:
            product = Product.objects.all()
            serializer = ProductListSerializer(product, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        product = Product.objects.get(id=pk)
        product.delete()
        return Response('Item deleted', status=status.HTTP_204_NO_CONTENT)