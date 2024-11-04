from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet, DefaultRecipientViewSet, ContactView,
    RegisterView, LoginView, LogoutView, ProfileView, EditProfileView,
    ChangePasswordView, PasswordResetView, PasswordResetConfirmView,
    VerifyEmailView, ActivateView, VerifyPhoneView, InputVerificationCodeView,
    PrivacyPolicyView, DataDeletionView
)

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'defaultrecipients', DefaultRecipientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', ContactView.as_view(), name='contact'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('verify-phone/', VerifyPhoneView.as_view(), name='verify_phone'),
    path('input-verification-code/', InputVerificationCodeView.as_view(), name='input_verification_code'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('data-deletion/', DataDeletionView.as_view(), name='data_deletion'),
]