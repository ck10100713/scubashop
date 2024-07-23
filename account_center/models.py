from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class DefaultRecipient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=100)
    recipient_phone_number = models.CharField(max_length=20)
    recipient_address = models.TextField()

    def __str__(self):
        return self.user.username