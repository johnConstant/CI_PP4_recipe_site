from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.defaultfilters import slugify
from .forms import RecipeForm, IngredientForm, InstructionForm
from .models import Recipe


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_date')
    template_name = 'recipes.html'
    paginate_by = 12


class RecipeDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)

        context = {
            'recipe': recipe,
        }
        return render(request, 'recipe_detail.html', context)


class AddRecipe(View):

    def get(self, request, *args, **kwargs):
        context = {
            'recipe_form': RecipeForm(),
            'instruction_form': InstructionForm(),
            'ingredient_form': IngredientForm()
        }
        return render(request, 'add_recipe.html', context)

    def post(self, request, *args, **kwargs):
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredient_form = RecipeForm(request.POST)
        instruction_form = RecipeForm(request.POST)

        recipe_form.instance.slug = slugify(request.POST['title'])
        if (
            recipe_form.is_valid() and
            ingredient_form.is_valid() and
            instruction_form.is_valid()
        ):
            recipe_form.instance.author = request.user
            recipe = recipe_form.save()
            instructions = instruction_form.save(False)
            instructions.recipe = recipe
            # instructions.save()
            ingredients = ingredient_form.save(False)
            ingredients.recipe = recipe
            # ingredients.save()
            print(recipe)
            return HttpResponseRedirect('/recipes/')


class EditRecipe(View):

    def get(self, request, slug, *args, **kwargs):
        recipe = get_object_or_404(Recipe, slug=slug)
        form = RecipeForm(instance=recipe)
        context = {
            'recipe_form': form,
            'instruction_form': InstructionForm(instance=recipe),
            'ingredient_form': IngredientForm(instance=recipe)
        }
        return render(request, 'edit_recipe.html', context)

    # def post(self, request, slug, *args, **kwargs):
    #     recipe = get_object_or_404(Recipe, slug=slug)
    #     recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
    #     ingredient_form = RecipeForm(request.POST, instance=recipe)
    #     instruction_form = RecipeForm(request.POST, instance=recipe)

    #     recipe_form.instance.slug = slugify(request.POST['title'])
    #     if (
    #         recipe_form.is_valid() and
    #         ingredient_form.is_valid() and
    #         instruction_form.is_valid()
    #     ):
    #         recipe_form.instance.author = request.user
    #         recipe = recipe_form.save()
    #         instructions = instruction_form.save(False)
    #         instructions.recipe = recipe
    #         # instructions.save()
    #         ingredients = ingredient_form.save(False)
    #         ingredients.recipe = recipe
    #         # ingredients.save()
    #         print(recipe)
    #         return HttpResponseRedirect('/recipes/')


class RecipeDelete(View):
    """
    A class view for deleting existing recipe
    """
    def post(self, request, id, **kwargs):
        """
        Delete a selected recipe
        """
        try:
            recipe = Recipe.objects.get(id=id)
            recipe.delete()
            messages.success(request, "Your recipe has been deleted.")
            return redirect('recipes')
        except recipe.DoesNotExist:
            messages.error(request,
                           'An error occurred when deleting your recipe.')
            return redirect('recipes')
