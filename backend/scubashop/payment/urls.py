from django.urls import path
from .views import PaymentProcessView, PaymentDoneView, PaymentCanceledView, PayPalWebhookView

urlpatterns = [
    path('process/<int:order_id>/', PaymentProcessView.as_view(), name='payment_process'),
    path('done/', PaymentDoneView.as_view(), name='payment_done'),
    path('canceled/', PaymentCanceledView.as_view(), name='payment_canceled'),
    path('webhook/', PayPalWebhookView.as_view(), name='paypal_webhook'),
]