from django.contrib import admin
from .models import UserProfile, DefaultRecipient


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone_number', 'email', 'email_verified', 'phone_verified')

class DefaultRecipientAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipient_name', 'recipient_phone_number', 'recipient_address')

# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DefaultRecipient, DefaultRecipientAdmin)