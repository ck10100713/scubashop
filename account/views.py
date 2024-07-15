from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.shortcuts import get_object_or_404
from .forms import UserProfileForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, recipient_name='', phone_number='', address='')
            login(request, user)
            return redirect('/')
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

@login_required
def profile_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'account/profile_page.html', {'user_profile': user_profile})

# @login_required
# def edit_profile(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             return redirect('account:profile')  # 重定向到個人資料頁面
#     else:
#         form = UserProfileForm(instance=user_profile)
#     return render(request, 'account/edit_profile.html', {'form': form})

@login_required
def edit_profile(request):
    User = get_user_model()
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('account:profile')  # 重定向到個人資料頁面
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'account/edit_profile.html', {'form': form, 'user_profile': user_profile, 'user': user})

@login_required
def change_password(request):
    # 可以在這裡修改用戶的密碼
    return render(request, 'account/changepassword.html')