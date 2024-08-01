from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from shop.models import Product
from orders.models import Order
from .forms import PaymentForm

def payment_process(request, order_id):
    # order = get_object_or_404(Order, id=order_id)
    try:
        order = get_object_or_404(Order, id=order_id)
    except Order.DoesNotExist:
        # 處理訂單不存在的情況
        return render(request, 'payment/error.html', {'error': 'Order not found'})
    paypal_dict = {
        "business": "your-paypal-business-email@example.com",
        "amount": str(order.get_total_cost()),
        "item_name": f"Order {order.id}",
        "invoice": str(order.id),
        "currency_code": "USD",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('payment_canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': order, 'form': form})

def payment_done(request):
    return render(request, 'payment/payment_done.html')

def payment_canceled(request):
    return render(request, 'payment/payment_canceled.html')