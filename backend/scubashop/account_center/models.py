from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    facebook_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    line_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    registration_method = models.CharField(max_length=50, choices=[
        ('local', 'Local'), ('google', 'Google'), ('line', 'Line'), ('facebook', 'Facebook'),
    ], default='local')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.email_verified:
            # 清除未驗證的重複 email
            UserProfile.objects.filter(
                email=self.email,
                email_verified=False
            ).exclude(id=self.id).update(email='')
        super().save(*args, **kwargs)

    def link_oauth_account(self, provider, uid):
        if provider == 'google':
            existing_profile = UserProfile.objects.filter(google_id=uid).first()
        elif provider == 'facebook':
            existing_profile = UserProfile.objects.filter(facebook_id=uid).first()
        elif provider == 'line':
            existing_profile = UserProfile.objects.filter(line_id=uid).first()
        else:
            return

        if existing_profile:
            if existing_profile.user != self.user:
                # Handle conflicting cases or merge accounts
                raise ValueError("This OAuth account is already linked to another user.")
            else:
                # Update existing profile with new provider info if needed
                if provider == 'google':
                    self.google_id = uid
                elif provider == 'facebook':
                    self.facebook_id = uid
                elif provider == 'line':
                    self.line_id = uid
                self.save()
        else:
            # Link the OAuth account to the current profile
            if provider == 'google':
                self.google_id = uid
            elif provider == 'facebook':
                self.facebook_id = uid
            elif provider == 'line':
                self.line_id = uid
            self.save()

class DefaultRecipient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=100)
    recipient_phone_number = models.CharField(max_length=20)
    recipient_address = models.TextField()

    def __str__(self):
        return self.user.username