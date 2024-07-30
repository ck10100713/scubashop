# account_center/adapter.py

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from .models import UserProfile, DefaultRecipient

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.save()
        # 创建 UserProfile 对象
        UserProfile.objects.get_or_create(user=user)
        # 其他逻辑
        if commit:
            user.save()
        return user

    def get_login_redirect_url(self, request):
        path = "/shop/index/"
        return path

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        # 调用父类的save_user方法
        user = super().save_user(request, sociallogin, form=form)
        # 获取或创建用户的 UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        # 将 email_verified 设置为 True
        profile.email_verified = True
        profile.save()
        return user

    def get_login_redirect_url(self, request):
        path = "/shop/index/"
        return path