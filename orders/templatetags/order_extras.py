from django import template

register = template.Library()

@register.filter
def get_total_cost(cart):
    # 实现您的逻辑来计算总费用
    total_cost = 0
    for item in cart:
        total_cost += item.goods.price * item.amount
    return total_cost
