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
        user = sociallogin.user
        user.save()
        # 创建 UserProfile 对象
        UserProfile.objects.get_or_create(user=user)
        # 更新用户的其他信息，例如email_verified
        socialaccount = SocialAccount.objects.filter(user=user, provider=sociallogin.account.provider).first()
        if socialaccount:
            user.email_verified = True
            user.save()
        return user

    def get_login_redirect_url(self, request):
        path = "/shop/index/"
        return path