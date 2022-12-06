import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.forms import formset_factory

from .forms import RecipeForm, IngredientForm, InstructionForm, CommentForm
from .models import Recipe, Ingredient, Instruction


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('created_date')
    template_name = 'recipes.html'
    paginate_by = 6


class RecipeDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        ingredients_list = Ingredient.objects.filter(recipe=recipe)
        instructions_list = Instruction.objects.filter(recipe=recipe)
        comments = recipe.comments.filter(approved=True).order_by(
            'created_date')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = {
            'recipe': recipe,
            'ingredients_list': ingredients_list,
            'instructions_list': instructions_list,
            'comments': comments,
            'commented': False,
            'liked': liked,
            'comment_form': CommentForm()
        }
        return render(request, 'recipe_detail.html', context)

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by(
            'created_date')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.Recipe = Recipe
            comment.save()
        else:
            comment_form = CommentForm()

        context = {
            'recipe': recipe,
            'comments': comments,
            'commented': True,
            'liked': liked,
            'comment_form': CommentForm()
        }
        return render(request, 'recipe_detail.html', context)


class RecipeLike(View):

    def post(self, request, slug, *args, **kwargs):
        recipe = get_object_or_404(Recipe, slug=slug)
        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)

        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


class AddRecipe(View):
    """
    A class view for adding a recipe
    """
    def get(self, request, *args, **kwargs):
        form = RecipeForm()
        Ingredient_formset = formset_factory(
            IngredientForm, extra=10, validate_min=True
            )
        Instruction_formset = formset_factory(
            InstructionForm, extra=5, validate_min=True
            )

        context = {
            'recipe_form': form,
            'instruction_form': InstructionForm(),
            'ingredient_form': IngredientForm()
        }
        return render(request, 'add_recipe.html', context)

    def post(self, request, *args, **kwargs):
        recipe_form = RecipeForm(request.POST, request.FILES)
        Ingredient_formset = formset_factory(
            IngredientForm, extra=10, validate_min=True
            )
        Instruction_formset = formset_factory(
            InstructionForm, extra=5, validate_min=True
            )
        instruction_formset = Instruction_formset(request.POST)
        ingredient_formset = Ingredient_formset(request.POST)

        recipe_form.instance.slug = slugify(request.POST['title'])

        if recipe_form.is_valid():
            try:
                recipe_form.instance.author = request.user
                recipe = recipe_form.save()
                if instruction_formset.is_valid():
                    for instruction_form in instruction_formset:
                        instructions = instruction_form.save(False)
                        instructions.recipe = recipe
                        if instructions.body != '':
                            instructions.save()
                print('hello')
                if ingredient_formset.is_valid():
                    for ingredient_form in ingredient_formset:
                        ingredient = ingredient_form.save(False)
                        ingredient.recipe = recipe
                        # if ingredient.name != '':
                        #     print(ingredient.name)
                        ingredient.save()

                messages.success(request, 'Your recipe has been created.')
                return HttpResponseRedirect('/recipes/')

            except recipe.DoesNotExist:
                messages.error(request, 'An error occurred adding your recipe')
                return HttpResponseRedirect('/recipes/')
        else:
            context = {
                'recipe_form': form,
                'instruction_form': InstructionForm(),
                'ingredient_form': IngredientForm()
            }
        return render(request, 'add_recipe.html', context)
        # return HttpResponseRedirect('/')


class EditRecipe(View):
    """
    A class view for updating an existing recipe
    """
    def get(self, request, slug, *args, **kwargs):

        recipe_id = self.kwargs['slug']
        recipe = Recipe.objects.get(slug=recipe_id)
        form = RecipeForm(instance=recipe)
        instructionForms = formset_factory(
            InstructionForm, extra=5, validate_min=True
            )

        if request.user == recipe.author:
            instructions = Instruction.objects.filter(recipe=recipe)
            instruction_fields = formset_factory(InstructionForm, extra=3)
            field_value = []
            for instruction in instructions:
                field_value.append({'body': instruction.body})
            instruction_formset = instruction_fields(initial=field_value)

            ingredients = Ingredient.objects.filter(recipe=recipe)
            ingredient_fields = formset_factory(IngredientForm, extra=5)
            ingredient_field_value = []
            for ingredient in ingredients:
                ingredient_field_value.append(
                    {
                        'amount': ingredient.amount,
                        'name': ingredient.name,
                        'notes': ingredient.notes
                    }
                )
            ingredient_formset = ingredient_fields(
                initial=ingredient_field_value
                )

        context = {
            'recipe_form': form,
            'instruction_form': instruction_formset,
            'ingredient_form': ingredient_formset,
        }
        return render(request, 'edit_recipe.html', context)

    def post(self, request, slug, *args, **kwargs):
        recipe_id = self.kwargs['slug']
        recipe = Recipe.objects.get(slug=recipe_id)
        recipe_form = RecipeForm(request.POST, request.FILES)
        Ingredient_formset = formset_factory(
            IngredientForm, extra=10, validate_min=True
            )
        Instruction_formset = formset_factory(
            InstructionForm, extra=5, validate_min=True
            )
        instruction_formset = Instruction_formset(request.POST)
        ingredient_formset = Ingredient_formset(request.POST)

        if recipe_form.is_valid():
            try:
                recipe_form.instance.author = request.user
                recipe_form.instance.last_modifed = datetime.date.today()
                recipe_form.instance.slug = slugify(request.POST['title'])
                recipe = recipe_form.save()
                if instruction_formset.is_valid():
                    for instruction_form in instruction_formset:
                        instructions = instruction_form.save(False)
                        instructions.recipe = recipe
                        if instructions.body != '':
                            instructions.save()
                if ingredient_formset.is_valid():
                    for ingredient_form in ingredient_formset:
                        ingredient = ingredient_form.save(False)
                        ingredient.recipe = recipe
                        ingredient.save()

                messages.success(request, 'Your recipe has been updated.')
                return HttpResponseRedirect('/recipes/')

            except recipe.DoesNotExist:
                messages.error(request, 'An error occurred adding your recipe')
                return HttpResponseRedirect('/recipes/')

        return HttpResponseRedirect('/')


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
