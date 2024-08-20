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
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False, label="分類"
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(), required=False, label="品牌"
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('', '-------------'),  # 這裡加入空選項
            ('price_asc', '金額：低到高'),
            ('price_desc', '金額：高到低'),
        ],
        required=False,
        label="排序"
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']