from django import forms
from django.forms import ModelForm
from main.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "category", "thumbnail"]
        widgets = {
            "name": forms.widgets.TextInput(attrs={'class': 'form-control'}),
            "price": forms.widgets.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            "description": forms.widgets.TextInput(attrs={'class': 'form-control'}),
            "thumbnail": forms.widgets.URLInput(attrs={'class': 'form-control'}),
            "category": forms.widgets.Select(attrs={'class': 'form-select'}),
        }


form = ProductForm()
for field in form:
    field.field.widget.attrs
