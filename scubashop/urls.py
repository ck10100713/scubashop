"""
URL configuration for scubashop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from shop.views import index_views
from django.conf import settings
from django.conf.urls.static import static
# from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title="Scuba Shop API",
        default_version='v1',
        description="Scuba Shop API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="penguin.divingclub@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_views, name='index'),
    path('shop/', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('account_center/', include('account_center.urls')),
    path('orders/', include('orders.urls')),
    path('payment/', include('payment.urls')),
    # api
    # path('api/', include('shop.urls')),
    # path('api/', include('orders.urls')),
    # oauth
    path('accounts/', include('allauth.urls')),
    # paypal payments
    # path('paypal/', include('paypal.standard.ipn.urls')),
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc UI (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)