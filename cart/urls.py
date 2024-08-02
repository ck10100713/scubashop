from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    # api
    path('api/', views.api_overview, name='api_overview'),
    path('api/cart/all', views.cart_list, name='cart_list'),
    path('api/cart/<int:user_id>/', views.list_cart, name='list_cart'),
]
