from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from orders.models import Order  # 假設你的訂單模型在 `shop` 應用中

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'Completed':
        # 支付成功，更新訂單狀態
        order = Order.objects.get(id=ipn_obj.invoice)
        order.status = 'PAID'
        order.save()