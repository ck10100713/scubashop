from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from shop.models import Product
from orders.models import Order
from .forms import PaymentForm
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk


paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox 或 live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

# def payment_process(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     total = str(order.get_total_cost())

#     paypal_dict = {
#         "business": settings.PAYPAL_RECEIVER_EMAIL,
#         "amount": total,
#         "item_name": "Order #{}".format(order_id),
#         "invoice": str(order_id),
#         "currency_code": "TWD",
#         "notify_url": request.build_absolute_uri(reverse('payment:paypal-ipn')),
#         "return_url": request.build_absolute_uri(reverse('payment:payment_done')),
#         "cancel_return": request.build_absolute_uri(reverse('payment:payment_canceled')),
#     }

#     form = PayPalPaymentsForm(initial=paypal_dict)
#     context = {"form": form}
#     return render(request, "payment/process.html", context)

# that is worked
from django.http import HttpResponse
from paypal.standard.forms import PayPalPaymentsForm

# def payment_process(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     total = str(order.get_total_cost())
#     paypal_dict = {
#         "business": settings.PAYPAL_RECEIVER_EMAIL,
#         "amount": total,
#         "item_name": "Order #{}".format(order_id),
#         "invoice": str(order_id),
#         "currency_code": "TWD",
#         "notify_url": request.build_absolute_uri(reverse('payment:paypal-ipn')),
#         "return_url": request.build_absolute_uri(reverse('payment:payment_done')),
#         "cancel_return": request.build_absolute_uri(reverse('payment:payment_canceled')),
#     }
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     # 渲染表單成 HTML 字符串
#     form_html = form.render()
#     # 返回渲染的 HTML 作為 HttpResponse
#     return HttpResponse(form_html)

# def payment_process(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     total = str(order.get_total_cost())
#     paypal_dict = {
#         "business": settings.PAYPAL_RECEIVER_EMAIL,
#         "amount": total,
#         "item_name": "Order #{}".format(order_id),
#         "invoice": str(order_id),
#         "currency_code": "TWD",
#         "notify_url": request.build_absolute_uri(reverse('payment:paypal-ipn')),
#         "return_url": request.build_absolute_uri(reverse('payment:payment_done')),
#         "cancel_return": request.build_absolute_uri(reverse('payment:payment_canceled')),
#     }
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     # 渲染表單成 HTML 字符串
#     form_html = form.render()

#     # 在 form_html 之前和之後添加自定義內容
#     custom_html_before = """
#     <html>
#     <head>
#         <title>付款處理</title>
#         <link rel="stylesheet" href="path_to_your_stylesheet.css">
#     </head>
#     <body>
#         <div class="container mt-5">
#             <h1 class="mb-4">訂單 #{} - 付款</h1>
#             <p class="mb-4">總金額：$ {}</p>
#     """.format(order_id, total)

#     custom_html_after = """
#             <p class="mt-3">
#                 <a href="{}" class="btn btn-secondary">取消並返回購物車</a>
#             </p>
#         </div>
#     </body>
#     </html>
#     """.format(reverse('cart:cart_detail'))

#     # 組裝完整的 HTML
#     full_html = custom_html_before + form_html + custom_html_after

#     # 返回組裝的 HTML 作為 HttpResponse
#     return HttpResponse(full_html)

# def payment_done(request):
#     return render(request, 'payment/payment_done.html')

# def payment_canceled(request):
#     return render(request, 'payment/payment_canceled.html')

def paypal_ipn(request):
    return HttpResponse('IPN received')

def payment_process(request):
    order_id = request.session.get('order_id')
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
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": str(order.amount),
                    "currency": "USD"},
                "description": f"Order {order.id} payment."}]})

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            return render(request, 'payment/error.html', {'error': payment.error})

    return render(request, 'payment/process.html', {'order': order})

def payment_done(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.paid = True
        order.save()
        return render(request, 'payment/done.html', {'order': order})
    else:
        return render(request, 'payment/error.html', {'error': payment.error})


def payment_canceled(request):
    return render(request, 'payment/canceled.html')