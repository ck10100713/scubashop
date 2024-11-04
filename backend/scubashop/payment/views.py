from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404, redirect
from orders.models import Order
import paypalrestsdk
from .paypal_config import configure_paypal
import json

# config
configure_paypal()

class PaymentProcessView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if order.user == request.user or request.user.is_staff:
            if order.paid:
                return Response({'error': '訂單已經支付過'}, status=status.HTTP_400_BAD_REQUEST)

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": request.build_absolute_uri('/api/payment/done/'),
                    "cancel_url": request.build_absolute_uri('/api/payment/canceled/')},
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
                        return Response({'approval_url': approval_url}, status=status.HTTP_200_OK)
            else:
                return Response({'error': payment.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': '您無權查看此頁面'}, status=status.HTTP_403_FORBIDDEN)

class PaymentDoneView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            order_id = request.session.get('order_id')
            if not order_id:
                return Response({'error': '缺少訂單ID'}, status=status.HTTP_400_BAD_REQUEST)
            order = get_object_or_404(Order, id=order_id)
            order.paid = True
            order.save()
            del request.session['order_id']
            return Response({'message': '支付成功', 'order': order.id}, status=status.HTTP_200_OK)
        else:
            return Response({'error': payment.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentCanceledView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'message': '支付已取消'}, status=status.HTTP_200_OK)

# Webhook (未測試)
class PayPalWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload = json.loads(request.body)
        event_type = payload.get('event_type')
        if event_type == 'PAYMENT.SALE.COMPLETED':
            sale_id = payload['resource']['id']
            # 更新訂單狀態
            # 例如：查找訂單並標記為已支付
        # 處理其他事件
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)