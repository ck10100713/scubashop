from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    # 当用户通过第三方登录时创建一个新的 UserProfile
    UserProfile.objects.get_or_create(user=user)


@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    # 用户登录后你可以执行一些操作
    pass