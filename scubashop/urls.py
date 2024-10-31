from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="API 文檔",
        default_version='v1',
        description="API 說明",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API 路由
    path('api/shop/', include('shop.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/account_center/', include('account_center.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/payment/', include('payment.urls')),
    # OAuth 路由
    path('accounts/', include('allauth.urls')),
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc UI (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)