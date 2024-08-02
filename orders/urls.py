# order/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('check/', views.order_check, name='check'),
    path('create/', views.order_create, name='create'),
    path('detail/<int:order_id>/', views.order_detail, name='detail'),
    path('history/', views.order_history, name='history'),
    # api
    path('api/', views.api_overview, name='order_api'),
    path('api/orderbooks', views.orderbooks, name='order'),
    path('api/orderbooks/<str:pk>/', views.orderbooks, name='order-detail'),
]