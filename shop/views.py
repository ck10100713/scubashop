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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import GoodsSerializer, GoodsTypeSerializer
from rest_framework import status, permissions


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Goods List': '/goods-list/',
        'Goods Detail': '/goods/<str:pk>/',
        'Goods Update': '/goods-update/<str:pk>/',
        'Goods Create': '/goods-create/',
        'Goodstype List': '/goodstype-list/',
        'Goodstype Detail': '/goodstype/<str:pk>/',
        'Goodstype Update': '/goodstype-update/<str:pk>/',
        'Goodstype Create': '/goodstype-create/',
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

@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def goods_create(request):
    serializer = GoodsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([permissions.IsAuthenticated])
@api_view(['PATCH'])
def goods_update(request, id):
    school = Goods.objects.get(id=id)
    serializer = GoodsSerializer(instance=school, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def goodstype_list(request):
    goodstype = GoodsType.objects.all()
    serializer = GoodsTypeSerializer(goodstype, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def goodstype_detail(request, pk):
    goodstype = GoodsType.objects.get(id=pk)
    serializer = GoodsTypeSerializer(goodstype, many=False)
    return Response(serializer.data)

@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def goodstype_create(request):
    serializer = GoodsTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([permissions.IsAuthenticated])
@api_view(['PATCH'])
def goodstype_update(request, id):
    school = GoodsType.objects.get(id=id)
    serializer = GoodsTypeSerializer(instance=school, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)