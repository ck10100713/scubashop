from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import UserProfile, DefaultRecipient
from django.core.validators import RegexValidator
import re

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="使用者名稱",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="信箱",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    cell_phone = forms.CharField(
        label="手機號碼",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(regex=r'^09\d{8}$', message='手機號碼格式錯誤')]
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'cell_phone', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(
        label="使用者名稱",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        # 設置空白欄位為選填
        fields_optional = ['phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_profile = kwargs.get('instance')
        if user_profile and user_profile.registration_method != 'local':
            self.fields['email'].widget.attrs['readonly'] = True

        # 設置 phone_number 為選填
        if 'phone_number' in self.fields:
            self.fields['phone_number'].required = False

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^09\d{8}$', phone_number):
            raise forms.ValidationError('電話號碼必須是以 09 開頭，並且有 10 位數字。')
        return phone_number

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if user_profile.phone_number and user_profile.phone_number != self.instance.phone_number:
            user_profile.phone_verified = False
        if commit:
            user_profile.save()
        return user_profile

class DefaultRecipientForm(forms.ModelForm):
    class Meta:
        model = DefaultRecipient
        fields = ['recipient_name', 'recipient_phone_number', 'recipient_address']
        widgets = {
            'recipient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'recipient_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'recipient_address': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 設置 recipient_name 和 recipient_address 為選填
        for field in ['recipient_name', 'recipient_phone_number', 'recipient_address']:
            if field in self.fields:
                self.fields[field].required = False

    def clean_recipient_phone_number(self):
        phone_number = self.cleaned_data.get('recipient_phone_number')
        if phone_number and not re.match(r'^09\d{8}$', phone_number):
            raise forms.ValidationError('電話號碼必須是以 09 開頭，並且有 10 位數字。')
        return phone_number


# for oauth
class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'})
        }
# password reset
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="電子郵件", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))