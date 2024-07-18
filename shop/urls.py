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
    path('index/', views.index_views, name='index'),
    path('', views.shop_views, name='shop'),
    # path('create_product/', views.create_product, name='create_product'),
    # path('create_category/', views.create_category, name='create_category'),
    path('product/<int:product_id>/', views.product_detail_views, name='product_detail'),
    path('photo/', views.photo_views, name='photo'),
    # api
    path('api/', views.api_overview, name='api-overview'),
    path('api/goods', views.goods, name='goods'),
    path('api/goods/<str:pk>/', views.goods, name='goods-detail'),
    path('api/goodstype', views.goodstype, name='goodstype'),
    path('api/goodstype/<str:pk>/', views.goodstype, name='goodstype-detail'),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)