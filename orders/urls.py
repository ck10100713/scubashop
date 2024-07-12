# order/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('api/', views.order_list_create, name='order_list_create'),
    path('api/<int:pk>/', views.order_detail, name='order_detail'),
    path('api/items/', views.order_item_list_create, name='order_item_list_create'),
    path('api/items/<int:pk>/', views.order_item_detail, name='order_item_detail'),
]