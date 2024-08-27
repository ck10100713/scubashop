from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, DefaultRecipient
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import UserProfileForm, DefaultRecipientForm, CompleteProfileForm
from django.http import HttpResponseRedirect
from django.contrib import messages


# def merge_accounts(email, new_user, auth_provider):
#     """
#     合併具有相同電子郵件的不同用戶帳戶。
#     """
#     try:
#         existing_user = User.objects.get(email=email)
#         if existing_user != new_user:
#             # 處理合併邏輯，例如將新用戶的數據合併到現有用戶中
#             # ...
#             # 提示用戶進行操作，這取決於具體需求
#             raise ValidationError(_('A user with this email already exists.'))
#     except User.DoesNotExist:
#         # 如果不存在現有用戶，則可以直接創建新用戶
#         new_user.save()

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             cell_phone = form.cleaned_data.get('cell_phone')
#             # 確認信箱是否已經存在
#             email = form.cleaned_data.get('email')
#             # if User.objects.filter(email=email).exists():

#             # merge_accounts(email, user, 'email')
#             UserProfile.objects.create(user=user, phone_number=cell_phone, email=user.email)
#             DefaultRecipient.objects.create(user=user)
#             user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默認的身份驗證後端
#             login(request, user)
#             return redirect('/')  # 注冊成功後重定向到首頁
#     else:
#         form = RegisterForm()
#     return render(request, 'account_center/register.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # 檢查是否已經有用戶驗證了此信箱
            if UserProfile.objects.filter(email=email, email_verified=True).exists():
                form.add_error('email', '此信箱已被註冊。')
            else:
                # 繼續處理註冊
                user = form.save()
                cell_phone = form.cleaned_data.get('cell_phone')

                # 創建 UserProfile 並且同步 email
                user_profile = UserProfile.objects.create(
                    user=user,
                    phone_number=cell_phone,
                    email=email
                )

                DefaultRecipient.objects.create(user=user)
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默認的身份驗證後端
                login(request, user)
                return redirect('/')  # 注冊成功後重定向到首頁
    else:
        form = RegisterForm()

    return render(request, 'account_center/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')  # 獲取 next 參數，預設為根目錄
                return redirect(next_url)  # 登录成功后重定向到 next 參數指定的頁面
            else:
                form.add_error(None, '無效的用戶名或密碼')
    else:
        form = LoginForm()
    return render(request, 'account_center/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        default_recipient = DefaultRecipient.objects.get(user=request.user)
    except DefaultRecipient.DoesNotExist:
        default_recipient = None

    return render(request, 'account_center/profile.html', {
        'user_profile': user_profile,
        'default_recipient': default_recipient,
    })

# @login_required
# def complete_profile_view(request):
#     user = request.user
#     user_profile, created = UserProfile.objects.get_or_create(user=user)
#     if request.method == 'POST':
#         form = CompleteProfileForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('account_center:profile')  # 重定向到用户的个人资料页面
#     else:
#         form = CompleteProfileForm(instance=user)
#     return render(request, 'account_center/complete_profile.html', {'form': form})

@login_required
def edit_profile_view(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    default_recipient, created = DefaultRecipient.objects.get_or_create(user=user)

    if request.method == 'POST':
        # 先保存當前的舊手機號碼
        old_phone_number = UserProfile.objects.get(user=user).phone_number

        # 初始化表單
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        recipient_form = DefaultRecipientForm(request.POST, instance=default_recipient)
        if profile_form.is_valid() and recipient_form.is_valid():
            # 保存表單數據到 user_profile
            profile_form.save()
            recipient_form.save()
            # 獲取清理過的新手機號碼
            new_phone_number = profile_form.cleaned_data.get('phone_number')
            # 比對新的手機號碼是否與舊的不同
            if old_phone_number != new_phone_number:
                user_profile.phone_verified = False
                user_profile.save()
            return redirect('account_center:profile')

        # 檢查表單是否有錯誤，並顯示對應的錯誤訊息
        elif recipient_form.is_valid():
            for errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f'基本資料出現錯誤 - {error}')
            recipient_form.save()
            return redirect('account_center:edit_profile')

        elif profile_form.is_valid():
            for errors in recipient_form.errors.items():
                for error in errors:
                    messages.error(request, f'收件人資料出現錯誤 - {error}')
            profile_form.save()
            return redirect('account_center:edit_profile')

        else:
            for errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f'基本資料出現錯誤 - {error}')
            for errors in recipient_form.errors.items():
                for error in errors:
                    messages.error(request, f'收件人資料出現錯誤 - {error}')
        return redirect('account_center:edit_profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        recipient_form = DefaultRecipientForm(instance=default_recipient)

    return render(request, 'account_center/edit_profile.html', {
        'profile_form': profile_form,
        'recipient_form': recipient_form,
        'user_profile': user_profile,
        'default_recipient': default_recipient,
        'user': user
    })

@login_required
def change_password_view(request):
    user = request.user
    if user.userprofile.registration_method != 'local':
        login_provider = user.userprofile.registration_method
        messages.error(request, '您的帳號是由{}登錄的，無法修改密碼。'.format(login_provider))
        return redirect('account_center:profile')
    else:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # 重要！更新用户的会话以防止注销
                return redirect('account_center:profile')
            else:
                # 表单无效，处理错误
                print(form.errors)
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'account_center/change_password.html', {'form': form})

# forgot password
from .forms import CustomPasswordResetForm
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from .tokens import generate_token, decode_token
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    if user.userprofile.registration_method != 'local':
                        messages.error(request, '您的帳號是由{}登錄的，無法重設密碼。'.format(user.userprofile.registration_method))
                        return redirect('account_center:password_reset')
                    else:
                        expiry_time = make_aware(datetime.now() + timedelta(days=1))  # 設定驗證連結有效期為 1 天
                        try:
                            token = generate_token(user, expiry_time)
                        except Exception as e:
                            messages.error(request, '密鑰生成失敗，請稍後再試。')
                            print(e)
                            return redirect('account_center:password_reset')
                        # token = default_token_generator.make_token(user)
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        current_site = get_current_site(request)

                        email_subject = '重設密碼請求'
                        text_message = render_to_string('account_center/password_reset_email.txt', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': uid,
                            'token': token,
                            'protocol': 'https' if request.is_secure() else 'http',
                            'reset_token_timeout': settings.PASSWORD_RESET_TIMEOUT_HOURS,
                        })
                        email_context = EmailMultiAlternatives(
                            email_subject,
                            text_message,
                            settings.EMAIL_HOST_USER,
                            [user.email]
                        )
                        try:
                            email_context.send()
                            messages.success(request, '重設密碼郵件已發送，請檢查您的郵箱。')
                        except Exception as e:
                            messages.error(request, '郵件發送失敗，請稍後再試。')
                            print(e)
    else:
        form = PasswordResetForm()

    return render(request, 'account_center/password_reset_form.html', {'form': form})

from django.contrib.auth.forms import SetPasswordForm

def password_reset_confirm_view(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        info = decode_token(token)
    except Exception as e:
        user = None
        info = {
            'user_id': None,
            'expiry': None
        }
        messages.error(request, '驗證連結無效。')
        return redirect('account_center:password_reset')
    # if user is not None and default_token_generator.check_token(user, token):
    if user is not None and user.id == info['user_id']:
        if info['expiry'] < datetime.now():
            messages.error(request, '驗證連結已過期，請重新申請。')
            return redirect('account_center:password_reset')
        else:
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, '密碼重設成功，請使用新密碼登入。')
                    return redirect('account_center:password_reset_complete')
            else:
                form = SetPasswordForm(user)
            return render(request, 'account_center/password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
    else:
        return render(request, 'account_center/password_reset_confirm_invalid.html')

def password_reset_complete_view(request):
    return render(request, 'account_center/password_reset_complete.html')

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode # 將二進制數據轉換為 URL 安全的 Base64 編碼
from django.utils.encoding import force_bytes
# from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib import messages
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

@login_required
def verify_email_view(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    # 處理驗證邏輯
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    expiry_time = make_aware(datetime.now() + timedelta(days=1))  # 設定驗證連結有效期為 1 天
    try:
        token = generate_token(user, expiry_time)
    except Exception as e:
        messages.error(request, '密鑰生成失敗，請稍後再試。')
        print(e)
        return redirect('account_center:profile')
    # token = account_activation_token.make_token(user)
    mail_subject = 'ScubaShop 會員帳號驗證'
    text_message = render_to_string('account_center/active_email.txt', {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
        'protocol': 'https' if request.is_secure() else 'http',
        'email_verification_token_timeout': settings.EMAIL_VERIFICATION_TIMEOUT_HOURS,
    })
    email = EmailMultiAlternatives(
        subject=mail_subject,
        body=text_message,  # 純文本內容
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    try:
        email.send()
        messages.success(request, '驗證郵件已發送，請檢查您的郵箱。')
    except Exception as e:
        print(e)
        messages.error(request, '郵件發送失敗，請稍後再試。')
    return redirect('account_center:profile')

from django.utils.http import urlsafe_base64_decode
from django.utils import timezone

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_profile = UserProfile.objects.get(user=user)
        info = decode_token(token)
    except Exception as e:
        print(e)
        user = None
        info = {
            'user_id': None,
            'expiry': None
        }
        messages.error(request, '驗證連結無效。')
        return redirect('account_center:profile')
    if user is not None and user.id == info['user_id']:
        if info['expiry'] < timezone.now():
            messages.error(request, '驗證連結已過期，請重新申請。')
            return redirect('account_center:profile')
        else:
            user_profile.email_verified = True
            user_profile.save()
            user_profile.user.email = user_profile.email
            user_profile.user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return render(request, 'account_center/activation_complete.html')
    else:
        return render(request, 'account_center/activation_invalid.html')

import boto3
import random

@login_required
def verify_phone(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.phone_verified:
        messages.error(request, '手機已驗證。')
        return redirect('account_center:profile')
    if not user_profile.phone_number:
        messages.error(request, '請先填寫手機號碼。')
        return redirect('account_center:edit_profile')
    phone_number = user_profile.phone_number
    # transform phone_number to E.164 format
    phone_number = '+886' + phone_number[1:]
    # 生成6位數驗證碼
    verification_code = str(random.randint(100000, 999999))
    request.session['phone_number'] = phone_number
    request.session['verification_code'] = verification_code
    sns_client = boto3.client('sns',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                    region_name=settings.AWS_DEFAULT_REGION
                                    )
    # 發送簡訊
    try:
        sns_client.publish(
            PhoneNumber=phone_number,
            Message=f"[Scubshop] 您的驗證碼為 {verification_code}（請於十分鐘內驗證）"
        )
        messages.success(request, '驗證碼已發送至您的手機，請查收。')
        return redirect('account_center:input_verification_code')
    except Exception as e:
        print(e)
        messages.error(request, '簡訊發送失敗，請稍後再試。')
        return redirect('account_center:profile')

def input_verification_code(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        if verification_code == request.session.get('verification_code'):
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            user_profile.phone_verified = True
            user_profile.save()
            messages.success(request, '手機驗證成功。')
            return redirect('account_center:profile')
        else:
            messages.error(request, '驗證碼錯誤，請重新輸入。')
    return render(request, 'account_center/input_verification_code.html')

# privacy-policy
def privacy_policy_view(request):
    return render(request, 'account_center/privacy_policy.html')

def data_deletion_view(request):
    return render(request, 'account_center/data_deletion.html')

from .forms import ContactForm
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            for_shop = {
                'subject': f'來自{name}的聯絡我們訊息',
                'message': message,
                'email' : settings.EMAIL_HOST_USER,
            }
            for_client = {
                'subject': 'ScubaShop 客服回覆',
                'message': f'親愛的{name}您好，感謝您的來信，我們已經收到您的訊息，我們將會盡快回覆您，謝謝！',
                'email': email,
            }
            # 發送郵件
            try:
                for_shop_email = EmailMultiAlternatives(
                    subject=for_shop['subject'],
                    body=for_shop['message'],
                    from_email=settings.EMAIL_HOST_USER,
                    to=[for_shop['email']],
                )
                for_shop_email.send()
                for_client_email = EmailMultiAlternatives(
                    subject=for_client['subject'],
                    body=for_client['message'],
                    from_email=settings.EMAIL_HOST_USER,
                    to=[for_client['email']]
                )
                for_client_email.send()
                messages.success(request, '您的訊息已成功發送！')
                return redirect('account_center:contact')
            except Exception as e:
                print(e)
                messages.error(request, '郵件發送失敗，請稍後再試。')
                return redirect('account_center:contact')
    else:
        form = ContactForm()
    return render(request, 'account_center/contact.html', {'form': form})


# api
from rest_framework import viewsets, permissions
from .models import UserProfile, DefaultRecipient
from .serializers import UserProfileSerializer, DefaultRecipientSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # 僅允許已驗證的用戶訪問

class DefaultRecipientViewSet(viewsets.ModelViewSet):
    queryset = DefaultRecipient.objects.all()
    serializer_class = DefaultRecipientSerializer
    permission_classes = [permissions.IsAuthenticated]