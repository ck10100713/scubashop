# account_center/adapter.py

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from .models import UserProfile
import random
import string
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        if commit:
            user.save()
            # 创建 UserProfile 对象
            UserProfile.objects.get_or_create(user=user)
        return user

    def get_login_redirect_url(self, request):
        return "/shop/index/"


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # 如果用戶已經登入，則不處理
        if request.user.is_authenticated:
            return

        # 嘗試根據email查找已存在的本地帳號
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                existing_user = User.objects.get(email=email)
                # 將這個社交帳號與現有的本地帳號關聯
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                # 如果沒有找到相同email的本地帳號，則允許創建新帳號
                pass

    def save_user(self, request, sociallogin, form=None):
        # 調用父類的 save_user 方法
        user = super().save_user(request, sociallogin, form=form)

        # 如果用戶名為空，自動生成一個
        if not user.username:
            user.username = self.generate_random_username(sociallogin.account.provider)
            user.save()

        # 創建或獲取 UserProfile 對象
        profile, created = UserProfile.objects.get_or_create(user=user, email=user.email)

        # 設置 email_verified 為 True
        profile.email_verified = True

        # 設置相應的 social ID
        if sociallogin.account.provider == 'google':
            profile.registration_method = 'google'
            profile.google_id = sociallogin.account.uid
        elif sociallogin.account.provider == 'facebook':
            profile.registration_method = 'facebook'
            profile.facebook_id = sociallogin.account.uid
        elif sociallogin.account.provider == 'line':
            profile.registration_method = 'line'
            profile.line_id = sociallogin.account.uid

        profile.save()

        return user

    def generate_random_username(self, provider):
        print('generate_random_username')
        """生成一個基於 provider 的隨機用戶名"""
        prefix = provider[0]  # 例如 'g' 對應 Google
        random_suffix = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}user{random_suffix}"

    def get_login_redirect_url(self, request):
        print('get_login_redirect_url')
        path = "/shop/index/"
        return path

    def populate_user(self, request, sociallogin, data):
        """
        自定義填充用戶信息的邏輯，包括自定義 username 生成
        """
        print('populate_user')
        user = super().populate_user(request, sociallogin, data)

        # 如果 `username` 已經被填充，則跳過這一步
        if not user.username:
            # 使用提供者的首字母 + 隨機數字生成唯一 `username`
            provider_prefix = sociallogin.account.provider[0]  # 例如 'g' 表示 Google
            random_suffix = ''.join(random.choices(string.digits, k=6))
            user.username = f"{provider_prefix}user{random_suffix}"

        return user
    def get_connect_redirect_url(self, request, socialaccount):
        # 登錄後重定向到 shop/index/
        return reverse('shop:index')

    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        # 當出現錯誤時，例如用戶取消了第三方登入，重定向到指定頁面
        print('authentication_error')
        return redirect('/shop/index/')