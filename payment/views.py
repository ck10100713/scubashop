# # payment/views.py
# from django.shortcuts import render, redirect
# from django.conf import settings
# from paypalrestsdk import Payment
# from .paypal_config import configure_paypal

# configure_paypal()

# def create_payment(request):
#     payment = Payment({
#         "intent": "sale",
#         "payer": {
#             "payment_method": "paypal"
#         },
#         "redirect_urls": {
#             "return_url": request.build_absolute_uri('/payment/execute/'),
#             "cancel_url": request.build_absolute_uri('/payment/cancel/')
#         },
#         "transactions": [{
#             "amount": {
#                 "total": "10.00",  # 此處填寫實際金額
#                 "currency": "USD"
#             },
#             "description": "This is the payment transaction description."
#         }]
#     })

#     if payment.create():
#         approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
#         return redirect(approval_url)
#     else:
#         return render(request, 'payment/error.html', {'error': payment.error})

# def execute_payment(request):
#     payment_id = request.GET.get('paymentId')
#     payer_id = request.GET.get('PayerID')
#     payment = Payment.find(payment_id)

#     if payment.execute({"payer_id": payer_id}):
#         return render(request, 'payment/success.html')
#     else:
#         return render(request, 'payment/error.html', {'error': payment.error})

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from shop.models import Product
from orders.models import Order

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    paypal_dict = {
        'business': 'ScubaShop_Paypal_Test@business.example.com',
        'amount': str(product.price),
        'item_name': product.name,
        'invoice': str(product.id),
        'currency_code': 'USD',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('payment_done')),
        'cancel_return': request.build_absolute_uri(reverse('payment_canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'shop/product_detail.html', {'product': product, 'form': form})

def payment_done(request):
    return render(request, 'payment/payment_done.html')

def payment_canceled(request):
    return render(request, 'payment/payment_canceled.html')

def payment_process(request):
    if request.method == 'POST':
        # 處理支付邏輯
        return redirect(reverse('payment:payment_done'))
    else:
        # 顯示支付表單
        form = PaymentForm()  # 假設這是你的支付表單
        return render(request, 'payment/payment_form.html', {'payment_form': form})