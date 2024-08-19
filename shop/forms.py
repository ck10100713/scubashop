from django import forms
from .models import Product, Category
from .models import Category, Brand

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'size', 'color', 'brand', 'image']

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select
    )
    
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,  # 如果品牌是可選的
        widget=forms.Select
    )

class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)
    sort_by = forms.ChoiceField(choices=[
        ('price_asc', '價格升序'),
        ('price_desc', '價格降序'),
    ], required=False)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']