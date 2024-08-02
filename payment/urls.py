from django.urls import path, include
from . import views

app_name = 'payment'

urlpatterns = [
    # path('process/<int:order_id>/', views.payment_process, name='payment_process'),
    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('paypal-ipn/', views.paypal_ipn, name='paypal-ipn'),  # 確保這裡有定義
]