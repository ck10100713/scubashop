from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, ProductImageViewSet, BrandViewSet, ShopView, ProductDetailView, PictureView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'brands', BrandViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product-detail/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('picture/<int:product_id>/', PictureView.as_view(), name='picture'),
]