from django import forms
from .models import Recipe, Ingredient, Instruction


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['created_date', 'last_modified', 'likes', 'author', 'slug']


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['body']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ['recipe']
