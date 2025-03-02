from django import forms
from .models import *

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'name', 
            'status', 
            'parent', 
            'description', 
            'image'
        ]


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = [
            'name', 
            'status', 
            'sku',
            'seller',
            'stock_quantity',
            'price',
            ''
            'description', 
            'image'
        ]

class DeleteCategoryForm(forms.Form):
    category_id = forms.IntegerField(widget=forms.HiddenInput())