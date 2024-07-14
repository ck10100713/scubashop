"""
URL configuration for scubashop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', views.index_views, name='index'),
    path('shop/', views.shop_views, name='shop'),
    path('product/<int:product_id>/', views.product_detail_views, name='product_detail'),
    path('get/shop_api', views.api_overview, name='api_overview'),
    path('get/goods', views.goods_list, name='goods_list'),
    path('get/goods/<int:pk>/', views.goods_detail, name='goods_detail'),
    path('create/goods', views.goods_create, name='goods_create'),
    path('update/goods/<int:pk>/', views.goods_update, name='goods_update'),
    path('get/goodstype', views.goodstype_list, name='goodstype_list'),
    path('get/goodstype/<int:pk>/', views.goodstype_detail, name='goodstype_detail'),
    path('create/goodstype', views.goodstype_create, name='goodstype_create'),
    path('update/goodstype/<int:pk>/', views.goodstype_update, name='goodstype_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)