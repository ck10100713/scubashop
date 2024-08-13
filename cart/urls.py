from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
router.register('cart', views.CartViewSet)

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    # api
    path('api/', include(router.urls)),  # 使用 DefaultRouter 生成的 API 路由
    # path('api/', views.api_overview, name='api_overview'),
    # path('api/cart/<int:user_id>/', views.list_cart, name='list_cart'),
]
