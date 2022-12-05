from django import forms
from django.forms import inlineformset_factory
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


InstructionFormSet = inlineformset_factory(
    parent_model=Recipe, model=Instruction,
    form=InstructionForm,
    extra=1, max_num=100, can_delete=False
)


class IngredientForm(forms.ModelForm):
    """
    A class view creating the Ingredients form
    """
    class Meta:
        model = Ingredient
        exclude = ['recipe']


IngredientFormSet = inlineformset_factory(
    parent_model=Recipe, model=Ingredient,
    form=IngredientForm,
    extra=1, max_num=100, can_delete=False
)


class CommentForm(forms.ModelForm):
    """
    A class view creating the Comment form
    """
    class Meta:
        model = Comment
        fields = ('body', )
