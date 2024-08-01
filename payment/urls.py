from django.urls import path, include
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/<int:order_id>/', views.payment_process, name='payment_process'),
    path('done/', views.payment_done, name='payment_done'),
    path('canceled/', views.payment_canceled, name='payment_canceled'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('paypal-ipn/', views.paypal_ipn, name='paypal-ipn'),  # 確保這裡有定義
]