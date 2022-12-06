from django import forms
from .models import Recipe, Ingredient, Instruction, Comment


class RecipeForm(forms.ModelForm):
    """
    A class view creating the Recipe form
    """
    class Meta:
        model = Recipe
        exclude = ['created_date', 'last_modified', 'likes', 'slug']


class InstructionForm(forms.ModelForm):
    """
    A class view creating the Instruction form
    """
    class Meta:
        model = Instruction
        fields = ['body']


class IngredientForm(forms.ModelForm):
    """
    A class view creating the Ingredients form
    """
    class Meta:
        model = Ingredient
        exclude = ['recipe']


class CommentForm(forms.ModelForm):
    """
    A class view creating the Comment form
    """
    class Meta:
        model = Comment
        fields = ('body', )
