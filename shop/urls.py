# """
# URL configuration for scubashop project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path
# from django.urls.conf import include
# from . import views
# from django.conf import settings
# from django.conf.urls.static import static

# app_name = 'shop'

# urlpatterns = [
#     path('index/', views.index_views, name='index'),
#     path('', views.shop_views, name='shop'),
#     path('product/<int:product_id>/', views.product_detail_views, name='detail'),
#     # api
#     path('api/', views.api_overview, name='api-overview'),
#     path('api/products', views.products, name='goods'),
#     path('api/products/<str:pk>/', views.products, name='goods-detail'),
# ]
# shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'shop'

router = DefaultRouter()
router.register('product', views.ProductViewSet)

urlpatterns = [
    # path('index/', views.index_views, name='index'),
    # path('', views.shop_views, name='shop'),
    # path('product/<int:product_id>/', views.product_detail_views, name='detail'),
    # # check picture
    # path('product/<int:product_id>/pictures/', views.picture_views, name='product_pictures'),
    # # API 路由
    # # path('api/', api_overview, name='api-overview'),
    # path('api/', include(router.urls)),  # 使用 DefaultRouter 生成的 API 路由
]