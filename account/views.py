from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, DefaultRecipient
from django.shortcuts import get_object_or_404
from .forms import UserProfileForm, DefaultRecipientForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            cell_phone = form.cleaned_data.get('cell_phone')
            # email = form.cleaned_data.get('email')
            UserProfile.objects.create(user=user, phone_number=cell_phone, email=user.email)
            DefaultRecipient.objects.create(user=user)
            login(request, user)
            return redirect('/')  # 注册成功后重定向到首页或其他页面
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})

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
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

# @login_required
# def profile_view(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     return render(request, 'account/profile_page.html', {'user_profile': user_profile})

@login_required
def profile_views(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    default_recipient = get_object_or_404(DefaultRecipient, user=request.user)
    return render(request, 'account/profile_page.html', {
        'user_profile': user_profile,
        'default_recipient': default_recipient
    })

# @login_required
# def edit_profile(request):
#     user = request.user
#     user_profile, created = UserProfile.objects.get_or_create(user=user)
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user_profile)
#         if form.is_valid():
#             print('save start')
#             form.save()
#             print('save scuccess')
#             return redirect('account:profile')  # 重定向到個人資料頁面
#     else:
#         print('save fail')
#         form = UserProfileForm(instance=user_profile)
#     return render(request, 'account/edit_profile.html', {'form': form, 'user_profile': user_profile, 'user': user})

@login_required
def edit_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    default_recipient, created = DefaultRecipient.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        recipient_form = DefaultRecipientForm(request.POST, instance=default_recipient)
        if profile_form.is_valid() and recipient_form.is_valid():
            profile_form.save()
            recipient_form.save()
            return redirect('account:profile')  # 重定向到個人資料頁面
    else:
        profile_form = UserProfileForm(instance=user_profile)
        recipient_form = DefaultRecipientForm(instance=default_recipient)

    return render(request, 'account/edit_profile.html', {
        'profile_form': profile_form,
        'recipient_form': recipient_form,
        'user_profile': user_profile,
        'default_recipient': default_recipient,
        'user': user
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 重要！更新用户的会话以防止注销
            return redirect('account:profile')
        else:
            # 表单无效，处理错误
            print(form.errors)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {'form': form})


@login_required
def verify_email(request):
    user_profile = request.user.userprofile
    # 處理驗證邏輯
    user_profile.email_verified = True
    user_profile.save()
    return redirect('account:edit_profile')

@login_required
def verify_phone(request):
    user_profile = request.user.userprofile
    # 處理驗證邏輯
    user_profile.phone_verified = True
    user_profile.save()
    return redirect('account:edit_profile')