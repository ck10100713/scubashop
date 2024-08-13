# account_center/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, DefaultRecipient

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'name', 'phone_number', 'email', 'email_verified', 'phone_verified']

class DefaultRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultRecipient
        fields = ['user', 'recipient_name', 'recipient_phone_number', 'recipient_address']