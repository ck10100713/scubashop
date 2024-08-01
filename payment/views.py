from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from shop.models import Product
from orders.models import Order
from .forms import PaymentForm
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template

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

def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total = str(order.get_total_cost())
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total,
        "item_name": "Order #{}".format(order_id),
        "invoice": str(order_id),
        "currency_code": "TWD",
        "notify_url": request.build_absolute_uri(reverse('payment:paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment:payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('payment:payment_canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    # 渲染表單成 HTML 字符串
    form_html = form.render()
    
    # 在 form_html 之前和之後添加自定義內容
    custom_html_before = """
    <html>
    <head>
        <title>付款處理</title>
        <link rel="stylesheet" href="path_to_your_stylesheet.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">訂單 #{} - 付款</h1>
            <p class="mb-4">總金額：$ {}</p>
    """.format(order_id, total)

    custom_html_after = """
            <p class="mt-3">
                <a href="{}" class="btn btn-secondary">取消並返回購物車</a>
            </p>
        </div>
    </body>
    </html>
    """.format(reverse('cart:cart_detail'))

    # 組裝完整的 HTML
    full_html = custom_html_before + form_html + custom_html_after
    
    # 返回組裝的 HTML 作為 HttpResponse
    return HttpResponse(full_html)

def payment_done(request):
    return render(request, 'payment/payment_done.html')

def payment_canceled(request):
    return render(request, 'payment/payment_canceled.html')

def paypal_ipn(request):
    return HttpResponse('IPN received')

# from django.shortcuts import render
# from .forms import PaymentForm
# from .paypal_client import PayPalClient  # 確保這個模塊正確導入

# def process_payment(request):
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             description = form.cleaned_data['description']
            
#             # 调用 PayPal 的 API 进行付款操作
#             paypal_client = PayPalClient()
#             payment_result = paypal_client.process_payment(amount, description)
            
#             if payment_result.success:
#                 # 付款成功，进行相应的处理
#                 # 更新数据库，发送邮件等
#                 return render(request, 'payment_success.html')
#             else:
#                 # 付款失败，返回错误信息给用户
#                 error_message = payment_result.error_message
#                 return render(request, 'payment_error.html', {'error_message': error_message})
#     else:
#         form = PaymentForm()
    
#     return render(request, 'payment_form.html', {'form': form})