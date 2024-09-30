# order/urls.py
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import include


router = DefaultRouter()
router.register('orders', views.OrderViewSet)

app_name = 'orders'

urlpatterns = [
    # path('check/', views.order_check, name='check'),
    # path('create/', views.order_create, name='create'),
    # path('detail/<int:order_id>/', views.order_detail, name='detail'),
    # path('history/', views.order_history, name='history'),
    # # api
    # path('api/', include(router.urls)),  # 使用 DefaultRouter 生成的 API 路由
    # # path('api/', views.api_overview, name='order_api'),
    # # path('api/orderbooks', views.orderbooks, name='order'),
    # # path('api/orderbooks/<str:pk>/', views.orderbooks, name='order-detail'),
]