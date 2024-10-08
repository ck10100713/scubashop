from django.contrib import admin
from .models import Cart

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','product',)
    list_filter = ('user', 'product')
    search_fields = ('user', 'product')

admin.site.register(Cart,CartAdmin)