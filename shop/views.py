from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Goods, GoodsType
from django.contrib.auth.forms import UserCreationForm

def index_views(request):
    products = Goods.objects.filter(isActive=True).order_by('-id')[:3]
    context = {
        'products': products
    }
    return render(request, 'index.html', context)

def shop_views(request):
    categories = GoodsType.objects.all()
    products = Goods.objects.filter(isActive=True)
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(goodsType_id=category_id)
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/shop.html', context)

def product_detail_views(request, product_id):
    product = get_object_or_404(Goods, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'shop/detail.html', context)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GoodsSerializer, GoodsTypeSerializer
from rest_framework import status

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Goods List': '/goods-list/',
        'Goods Detail': '/goods-detail/<str:pk>/',
        'Goods Create': '/goods-create/',
    }
    return Response(api_urls)

@api_view(['GET'])
def goods_list(request):
    goods = Goods.objects.all()
    serializer = GoodsSerializer(goods, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def goods_detail(request, pk):
    goods = Goods.objects.get(id=pk)
    serializer = GoodsSerializer(goods, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def goods_create(request):
    serializer = GoodsSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.validated_data)
        print('data saved')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def goods_update(request, pk):
#     try:
#         goods = Goods.objects.get(id=pk)
#     except Goods.DoesNotExist:
#         return Response({'error': 'Goods not found'}, status=status.HTTP_404_NOT_FOUND)

#     serializer = GoodsSerializer(instance=goods, data=request.data, partial=True)  # partial=True allows for partial updates
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def goods_update(request, id):
    school = Goods.objects.get(id=id)
    serializer = GoodsSerializer(instance=school, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)