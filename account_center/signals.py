from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up
from django.contrib.auth.models import User
from .models import UserProfile
from django.shortcuts import redirect

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    UserProfile.objects.get_or_create(user=user)
    return redirect('account_center:complete_profile')  # 重定向到自定义的 profile 页面

@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    return redirect('account_center:complete_profile')  # 重定向到自定义的 profile 页面