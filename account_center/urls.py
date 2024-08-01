from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account_center'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    # oauth
    path('complete_profile/', views.complete_profile_view, name='complete_profile'),
    # unfinished
    # path('profile/<int:pk>/', views.profile_views, name='profile'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('verify_phone/', views.verify_phone, name='verify_phone'),
    # api
]