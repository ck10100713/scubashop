from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserProfile, DefaultRecipient
from .serializers import UserProfileSerializer, DefaultRecipientSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from .tokens import generate_token, decode_token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # 僅允許已驗證的用戶訪問

class DefaultRecipientViewSet(viewsets.ModelViewSet):
    queryset = DefaultRecipient.objects.all()
    serializer_class = DefaultRecipientSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')

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
            return Response({'message': '您的訊息已成功發送！'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': '郵件發送失敗，請稍後再試。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        form = RegisterForm(request.data)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if UserProfile.objects.filter(email=email, email_verified=True).exists():
                return Response({'error': '此信箱已被註冊。'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = form.save()
                cell_phone = form.cleaned_data.get('cell_phone')
                user_profile = UserProfile.objects.create(
                    user=user,
                    phone_number=cell_phone,
                    email=email
                )
                DefaultRecipient.objects.create(user=user)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return Response({'message': '註冊成功'}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        form = LoginForm(request.data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return Response({'message': '登錄成功', 'next_url': next_url}, status=status.HTTP_200_OK)
            else:
                return Response({'error': '無效的用戶名或密碼'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': '登出成功'}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        default_recipient = get_object_or_404(DefaultRecipient, user=request.user)
        profile_serializer = UserProfileSerializer(user_profile)
        recipient_serializer = DefaultRecipientSerializer(default_recipient)
        return Response({
            'user_profile': profile_serializer.data,
            'default_recipient': recipient_serializer.data
        }, status=status.HTTP_200_OK)

class EditProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        default_recipient, created = DefaultRecipient.objects.get_or_create(user=user)

        old_phone_number = user_profile.phone_number

        profile_form = UserProfileForm(request.data, instance=user_profile)
        recipient_form = DefaultRecipientForm(request.data, instance=default_recipient)
        if profile_form.is_valid() and recipient_form.is_valid():
            profile_form.save()
            recipient_form.save()
            new_phone_number = profile_form.cleaned_data.get('phone_number')
            if old_phone_number != new_phone_number:
                user_profile.phone_verified = False
                user_profile.save()
            return Response({'message': '資料更新成功'}, status=status.HTTP_200_OK)
        errors = {**profile_form.errors, **recipient_form.errors}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.userprofile.registration_method != 'local':
            login_provider = user.userprofile.registration_method
            return Response({'error': f'您的帳號是由{login_provider}登錄的，無法修改密碼。'}, status=status.HTTP_400_BAD_REQUEST)
        form = PasswordChangeForm(user, request.data)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return Response({'message': '密碼修改成功'}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        form = PasswordResetForm(request.data)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    if user.userprofile.registration_method != 'local':
                        return Response({'error': f'您的帳號是由{user.userprofile.registration_method}登錄的，無法重設密碼。'}, status=status.HTTP_400_BAD_REQUEST)
                    expiry_time = make_aware(datetime.now() + timedelta(days=1))
                    try:
                        token = generate_token(user, expiry_time)
                    except Exception as e:
                        print(e)
                        return Response({'error': '密鑰生成失敗，請稍後再試。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                        return Response({'message': '重設密碼郵件已發送，請檢查您的郵箱。'}, status=status.HTTP_200_OK)
                    except Exception as e:
                        print(e)
                        return Response({'error': '郵件發送失敗，請稍後再試。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            info = decode_token(token)
        except Exception as e:
            print(e)
            return Response({'error': '驗證連結無效。'}, status=status.HTTP_400_BAD_REQUEST)
        if user is not None and user.id == info['user_id']:
            if info['expiry'] < datetime.now():
                return Response({'error': '驗證連結已過期，請重新申請。'}, status=status.HTTP_400_BAD_REQUEST)
            form = SetPasswordForm(user, request.data)
            if form.is_valid():
                form.save()
                return Response({'message': '密碼重設成功，請使用新密碼登入。'}, status=status.HTTP_200_OK)
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': '驗證連結無效。'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        expiry_time = make_aware(datetime.now() + timedelta(days=1))
        try:
            token = generate_token(user, expiry_time)
        except Exception as e:
            print(e)
            return Response({'error': '密鑰生成失敗，請稍後再試。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            body=text_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        try:
            email.send()
            return Response({'message': '驗證郵件已發送，請檢查您的郵箱。'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': '郵件發送失敗，請稍後再試。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActivateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            user_profile = UserProfile.objects.get(user=user)
            info = decode_token(token)
        except Exception as e:
            print(e)
            return Response({'error': '驗證連結無效。'}, status=status.HTTP_400_BAD_REQUEST)
        if user is not None and user.id == info['user_id']:
            if info['expiry'] < timezone.now():
                return Response({'error': '驗證連結已過期，請重新申請。'}, status=status.HTTP_400_BAD_REQUEST)
            user_profile.email_verified = True
            user_profile.save()
            user_profile.user.email = user_profile.email
            user_profile.user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return Response({'message': '帳號驗證成功'}, status=status.HTTP_200_OK)
        return Response({'error': '驗證連結無效。'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPhoneView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.phone_verified:
            return Response({'error': '手機已驗證。'}, status=status.HTTP_400_BAD_REQUEST)
        if not user_profile.phone_number:
            return Response({'error': '請先填寫手機號碼。'}, status=status.HTTP_400_BAD_REQUEST)
        phone_number = user_profile.phone_number
        phone_number = '+886' + phone_number[1:]
        verification_code = str(random.randint(100000, 999999))
        request.session['phone_number'] = phone_number
        request.session['verification_code'] = verification_code
        sns_client = boto3.client('sns',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                        region_name=settings.AWS_DEFAULT_REGION
                                        )
        try:
            sns_client.publish(
                PhoneNumber=phone_number,
                Message=f"[Scubshop] 您的驗證碼為 {verification_code}（請於十分鐘內驗證）"
            )
            return Response({'message': '驗證碼已發送至您的手機，請查收。'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': '簡訊發送失敗，請稍後再試。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InputVerificationCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        verification_code = request.data.get('verification_code')
        if verification_code == request.session.get('verification_code'):
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            user_profile.phone_verified = True
            user_profile.save()
            return Response({'message': '手機驗證成功。'}, status=status.HTTP_200_OK)
        return Response({'error': '驗證碼錯誤，請重新輸入。'}, status=status.HTTP_400_BAD_REQUEST)

class PrivacyPolicyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'message': '隱私政策內容'}, status=status.HTTP_200_OK)

class DataDeletionView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'message': '數據刪除政策內容'}, status=status.HTTP_200_OK)