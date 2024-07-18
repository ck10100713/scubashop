from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'categories', 'price', 'description', 'size', 'color', 'brand', 'image']

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']