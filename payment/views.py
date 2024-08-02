from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from orders.models import Order
import paypalrestsdk
from .paypal_config import configure_paypal
import json

# config
configure_paypal()

# Create your views here.
@login_required
def payment_process(request, order_id):
    # order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    if order.user == request.user or request.user.is_staff:
        # 確認訂單是否已經支付過
        if order.paid:
            return render(request, 'payment/already_paid.html', {'order': order})

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
    else:
        return render(request, 'payment/error.html', {'error': 'You are not authorized to view this page.'})

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

# webhook untested
# def paypal_webhook(request):
#     if request.method == 'POST':
#         payload = json.loads(request.body)
#         event_type = payload.get('event_type')
#         if event_type == 'PAYMENT.SALE.COMPLETED':
#             sale_id = payload['resource']['id']
#             # 更新訂單狀態
#             # 例如：查找訂單並標記為已支付
#         # 處理其他事件
#         return HttpResponse('OK')
#     return HttpResponse('Invalid request', status=400)

# def payment_detail(request, payment_id):
#     payment = get_object_or_404(Payment, id=payment_id)
#     return render(request, 'payment/detail.html', {'payment': payment})