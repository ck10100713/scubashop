from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderCheckView, OrderCreateView, OrderDetailView, OrderHistoryView

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('order-check/', OrderCheckView.as_view(), name='order_check'),
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-detail/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
]