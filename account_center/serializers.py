from rest_framework import serializers
from .models import UserProfile, DefaultRecipient

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class DefaultRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultRecipient
        fields = '__all__'