from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    """
    A class view creating the Category form
    """
    class Meta:
        model = Category
        fields = ['title', 'description', 'featured_image', 'status']
