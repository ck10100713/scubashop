from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category,CategoryAdmin)

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name','price','description','size','color','brand','image')
    search_fields = ('name',)
    list_filter = ('categories',)
    # readonly_fields = ('image',)

    def image(self, obj):
        return u'<img src="%s" height="150"/>' % obj.image.url
    
    image.allow_tags = True

admin.site.register(Product,ProductsAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product','image')
    search_fields = ('product',)
    list_filter = ('product',)

admin.site.register(ProductImage,ProductImageAdmin)