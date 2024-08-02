from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, DefaultRecipient
# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import UserProfileForm, DefaultRecipientForm, CompleteProfileForm
from django.http import HttpResponseRedirect

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            cell_phone = form.cleaned_data.get('cell_phone')
            # email = form.cleaned_data.get('email')
            UserProfile.objects.create(user=user, phone_number=cell_phone, email=user.email)
            DefaultRecipient.objects.create(user=user)
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默認的身份驗證後端
            login(request, user)
            return redirect('/')  # 注册成功后重定向到首页或其他页面
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

@login_required
def complete_profile_view(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_center:profile')  # 重定向到用户的个人资料页面
    else:
        form = CompleteProfileForm(instance=user)
    return render(request, 'account_center/complete_profile.html', {'form': form})

@login_required
def edit_profile_view(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    default_recipient, created = DefaultRecipient.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        recipient_form = DefaultRecipientForm(request.POST, instance=default_recipient)
        if profile_form.is_valid() and recipient_form.is_valid():
            profile_form.save()
            recipient_form.save()
            return redirect('account_center:profile')  # 重定向到個人資料頁面
        if  profile_form.is_valid():
            profile_form.save()
            return redirect('account_center:profile')
        if recipient_form.is_valid():
            recipient_form.save()
            return redirect('account_center:profile')
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

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode # 將二進制數據轉換為 URL 安全的 Base64 編碼
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib import messages
from django.utils.encoding import force_str
from django.contrib.auth.models import User
# from django.contrib.auth.tokens import default_token_generator

@login_required
def verify_email_view(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    # 處理驗證邏輯
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    mail_subject = 'ScubaShop 會員帳號驗證'

    text_message = render_to_string('account_center/active_email.txt', {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
    })

    email = EmailMultiAlternatives(
        subject=mail_subject,
        body=text_message,  # 純文本內容
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )

    email.send()
    messages.success(request, '驗證郵件已發送，請檢查您的郵箱。')
    return redirect('account_center:profile')

from django.utils.http import urlsafe_base64_decode
# from django.utils.encoding import force_text

def activate(request, uidb64, token):
    try:
        # 解碼 UID，這裡的 uid 是 User 的主鍵
        uid = force_str(urlsafe_base64_decode(uidb64))
        # 查詢 User 實例
        user = User.objects.get(pk=uid)
        # 查詢對應的 UserProfile
        user_profile = UserProfile.objects.get(user=user)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user_profile.email_verified = True
        user_profile.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return render(request, 'account_center/activation_complete.html')
    else:
        return render(request, 'account_center/activation_invalid.html')

@login_required
def verify_phone(request):
    user_profile = request.user.userprofile
    # 處理驗證邏輯
    user_profile.phone_verified = True
    user_profile.save()
    return redirect('account_center:edit_profile')