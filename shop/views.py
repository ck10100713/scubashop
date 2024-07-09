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