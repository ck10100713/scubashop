from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:goods_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:goods_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete/<int:goods_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
]
