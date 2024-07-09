from django.contrib import admin
from .models import Cart

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','goods',)
    list_filter = ('user', 'goods')
    search_fields = ('user', 'goods')

admin.site.register(Cart,CartAdmin)