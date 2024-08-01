from django.urls import path, include
from . import views

urlpatterns = [
    # paypal payments
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('done/', views.payment_done, name='payment_done'),
    path('canceled/', views.payment_canceled, name='payment_canceled'),
    path('process/', views.payment_process, name='payment_process'),  # 假設這是處理支付的視圖
]