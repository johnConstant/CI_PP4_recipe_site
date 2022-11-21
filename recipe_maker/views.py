from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.defaultfilters import slugify
from .forms import RecipeForm, IngredientForm, InstructionForm, CommentForm
from .models import Recipe, Ingredient, Instruction


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_date')
    template_name = 'recipes.html'
    paginate_by = 12


class RecipeDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        ingredients_list = Ingredient.objects.filter(recipe=recipe)
        instructions_list = Instruction.objects.filter(recipe=recipe)
        comments = recipe.comments.filter(approved=True).order_by('created_date')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = {
            'recipe': recipe,
            'ingredients_list': ingredients_list,
            'instructions_list': instructions_list,
            'comment_form': CommentForm(),
            'comments': comments,
            'commented': False,
            'liked': liked
        }
        return render(request, 'recipe_detail.html', context)

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        ingredients_list = Ingredient.objects.filter(recipe=recipe)
        instructions_list = Instruction.objects.filter(recipe=recipe)
        comments = recipe.comments.filter(approved=True).order_by('created_date')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
        else:
            comment_form = CommentForm()

        context = {
            'recipe': recipe,
            'ingredients_list': ingredients_list,
            'instructions_list': instructions_list,
            'comment_form': CommentForm(),
            'comments': comments,
            'commented': False,
            'liked': liked
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

    def post(self, request, slug, *args, **kwargs):
        recipe = get_object_or_404(Recipe, slug=slug)
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_form = RecipeForm(request.POST, instance=recipe)
        instruction_form = RecipeForm(request.POST, instance=recipe)

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
