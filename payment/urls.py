from django.urls import path, include
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/<int:order_id>/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
    # path('webhook/', views.payment_webhook, name='webhook'),
]