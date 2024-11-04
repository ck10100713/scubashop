# orders/filters.py
import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    product = django_filters.NumberFilter(field_name='items__product', lookup_expr='exact')

    class Meta:
        model = Order
        fields = ['user', 'paid', 'product']
