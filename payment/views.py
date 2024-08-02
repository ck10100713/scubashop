from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
import paypalrestsdk
from .paypal_config import configure_paypal

# config
configure_paypal()

# Create your views here.
def payment_process(request, order_id):
    # order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payment/done/'),
                "cancel_url": request.build_absolute_uri('/payment/canceled/')},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": f"Order {order.id}",
                        "sku": "item",
                        "price": str(order.amount),
                        "currency": "TWD",
                        "quantity": 1}]},
                "amount": {
                    "total": str(order.amount),
                    "currency": "TWD"},
                "description": f"Order {order.id} payment."}]})

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    request.session['order_id'] = order.id
                    return redirect(approval_url)
        else:
            return render(request, 'payment/error.html', {'error': payment.error})
    return render(request, 'payment/process.html', {'order': order})

def payment_done(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # 從 session 中獲取 order_id
        order_id = request.session.get('order_id')
        if not order_id:
            return render(request, 'payment/error.html', {'error': 'Order ID is missing'})
        order = get_object_or_404(Order, id=order_id)
        order.paid = True
        order.save()
        # 清除 session 中的 order_id
        del request.session['order_id']
        return render(request, 'payment/done.html', {'order': order})
    else:
        return render(request, 'payment/error.html', {'error': payment.error})

def payment_canceled(request):
    return render(request, 'payment/canceled.html')