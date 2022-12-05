import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.forms import formset_factory, inlineformset_factory

from .forms import RecipeForm, IngredientForm, InstructionForm, CommentForm, InstructionFormSet, IngredientFormSet
from .models import Recipe, Ingredient, Instruction


class RecipeList(generic.ListView):
    """
    A class view for getting all recipes
    """
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_date')
    template_name = 'recipes.html'
    paginate_by = 12


class RecipeDetail(View):
    """
    A class view for getting a specific recipe
    """
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
            'comment_form': CommentForm(),
            'comments': comments,
            'commented': False,
            'liked': liked
        }
        return render(request, 'recipe_detail.html', context)

    def post(self, request, slug, *args, **kwargs):
        """
        A class view for adding a comment to a specific recipe
        """
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        ingredients_list = Ingredient.objects.filter(recipe=recipe)
        instructions_list = Instruction.objects.filter(recipe=recipe)
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


# class AddRecipe(View):
#     """
#     A class view for adding a recipe
#     """
#     def get(self, request, *args, **kwargs):
#         Ingredient_formset = formset_factory(
#             IngredientForm, extra=10, validate_min=True
#             )
#         Instruction_formset = formset_factory(
#             InstructionForm, extra=5, validate_min=True
#             )

#         context = {
#             'recipe_form': RecipeForm(),
#             'instruction_form': Instruction_formset,
#             'ingredient_form': Ingredient_formset
#         }
#         return render(request, 'add_recipe.html', context)

#     def post(self, request, *args, **kwargs):
#         recipe_form = RecipeForm(request.POST, request.FILES)
#         Ingredient_formset = formset_factory(
#             IngredientForm, extra=10, validate_min=True
#             )
#         Instruction_formset = formset_factory(
#             InstructionForm, extra=5, validate_min=True
#             )
#         instruction_formset = Instruction_formset(request.POST)
#         ingredient_formset = Ingredient_formset(request.POST)

#         recipe_form.instance.slug = slugify(request.POST['title'])

#         if recipe_form.is_valid():
#             try:
#                 recipe_form.instance.author = request.user
#                 recipe = recipe_form.save()
#                 if instruction_formset.is_valid():
#                     for instruction_form in instruction_formset:
#                         instructions = instruction_form.save(False)
#                         instructions.recipe = recipe
#                         if instructions.body != '':
#                             instructions.save()
#                 if ingredient_formset.is_valid():
#                     for ingredient_form in ingredient_formset:
#                         ingredient = ingredient_form.save(False)
#                         ingredient.recipe = recipe
#                         # if ingredient.name != '':
#                         #     print(ingredient.name)
#                         ingredient.save()

#                 messages.success(request, 'Your recipe has been created.')
#                 return HttpResponseRedirect('/recipes/')

#             except recipe.DoesNotExist:
#                 messages.error(request, 'An error occurred adding your recipe')
#                 return HttpResponseRedirect('/recipes/')
#         # return HttpResponseRedirect('/')


# class EditRecipe(View):

    # template_name = 'recipes.html'
    # form_class = InstructionForm
    # model = Instruction

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     if self.request.method == 'POST':
    #         context['formset'] = InstructionFormSet(self.request.POST, instance=self.object)
    #     else:
    #         context['formset'] = InstructionFormSet(instance=self.object)

    #     return context

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     formset = context['formset']

    #     with transaction.atomic():
    #         self.object = form.save()

    #         if formset.is_valid():
    #             formset.instance = self.object
    #             formset.save()

    #     return redirect('recipes')



    # """
    # A class view for updating an existing recipe
    # """
    # def get(self, request, slug, *args, **kwargs):

    #     recipe_slug = self.kwargs['slug']
    #     recipe = Recipe.objects.get(slug=recipe_slug)
    #     form = RecipeForm(instance=recipe)
    #     instructionForms = inlineformset_factory(
    #         Recipe, Instruction, InstructionForm, extra=5, validate_min=True
    #         )

    #     if request.user == recipe.author:
    #         instructions = Instruction.objects.filter(recipe=recipe)
    #         instruction_fields = formset_factory(InstructionForm, extra=3)
    #         field_value = []
    #         for instruction in instructions:
    #             field_value.append({'body': instruction.body})
    #         instruction_formset = instruction_fields(initial=field_value)

    #         ingredients = Ingredient.objects.filter(recipe=recipe)
    #         ingredient_fields = formset_factory(IngredientForm, extra=5)
    #         ingredient_field_value = []
    #         for ingredient in ingredients:
    #             ingredient_field_value.append(
    #                 {
    #                     'amount': ingredient.amount,
    #                     'name': ingredient.name,
    #                     'notes': ingredient.notes
    #                 }
    #             )
    #         ingredient_formset = ingredient_fields(
    #             initial=ingredient_field_value
    #             )

    #     context = {
    #         'recipe_form': form,
    #         'instruction_form': instruction_formset,
    #         'ingredient_form': ingredient_formset,
    #     }
    #     return render(request, 'edit_recipe.html', context)

    # def post(self, request, slug, *args, **kwargs):
    #     Ingredient_formset = formset_factory(
    #         IngredientForm, extra=10, validate_min=True
    #         )
    #     Instruction_formset = formset_factory(
    #         InstructionForm, extra=5, validate_min=True
    #         )
    #     instruction_formset = Instruction_formset(request.POST)
    #     ingredient_formset = Ingredient_formset(request.POST)

    #     recipe = get_object_or_404(Recipe, slug=slug)
    #     recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
    #     recipe_form.instance.slug = slugify(request.POST['title'])
    #     recipe_form.instance.last_modifed = datetime.date.today()

    #     if recipe_form.is_valid():
    #         try:
    #             print(instruction_formset.management_form)
    #             recipe_form.instance.author = request.user
    #             recipe = recipe_form.save()
    #             if instruction_formset.is_valid():
    #                 for instruction_form in instruction_formset:
    #                     instructions = Instruction.objects.filter(
    #                         recipe=recipe)
    #                     # print(instruction)
    #                     for instruction in instructions:
    #                         form = InstructionForm(
    #                             request.POST, instance=instruction)
    #                         if form.is_valid():
    #                             instruction = form.save(False)
    #                             instruction.recipe = recipe
    #                             if instruction.body != '':
    #                                 instruction.save()
    #                             else:
    #                                 print(form.errors)
    #                                 print('invalid form 1')
    #                         else:
    #                             print(form.errors)
    #                             print('invalid form 2')
    #             else:
    #                 recipe_slug = self.kwargs['slug']
    #                 recipe = Recipe.objects.get(slug=recipe_slug)
    #                 form = RecipeForm(instance=recipe)

    #                 context = {
    #                     'recipe_form': form,
    #                     'instruction_form': instruction_formset,
    #                     'ingredient_form': ingredient_formset,
    #                 }
    #                 return render(request, 'edit_recipe.html', context)
    #         # if ingredient_formset.is_valid():
    #             #     for ingredient_form in ingredient_formset:
    #             #         ingredient = ingredient_form.save(False)
    #             #         ingredient.recipe = recipe
    #             #         ingredient.save()

    #             messages.success(request, 'Your recipe has been updated.')
    #             return HttpResponseRedirect('/recipes/')

    #         except recipe.DoesNotExist:
    #             messages.error(
    #                 request, 'An error occurred updating your recipe'
    #                 )
    #             return HttpResponseRedirect('/recipes/')

    #     return HttpResponseRedirect('/')
class RecipeInline():
    form_class = RecipeForm
    model = Recipe
    template_name = "add_recipe.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('recipes')

    def formset_ingredients_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        ingredients = formset.save(commit=False)
        # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for ingredient in ingredients:
            ingredient.recipe = self.object
            ingredient.save()

    def formset_instructions_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        instructions = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for instruction in instructions:
            instruction.recipe = self.object
            instruction.save()


class RecipeCreate(RecipeInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(RecipeCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'ingredients': IngredientFormSet(prefix='ingredients'),
                'instructions': InstructionFormSet(prefix='instructions'),
            }
        else:
            return {
                'ingredients': IngredientFormSet(self.request.POST or None, prefix='ingredients'),
                'instructions': InstructionFormSet(self.request.POST or None, prefix='instructions'),
            }


class RecipeUpdate(RecipeInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(RecipeUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'ingredients': IngredientFormSet(self.request.POST or None, instance=self.object, prefix='ingredients'),
            'instructions': InstructionFormSet(self.request.POST or None, instance=self.object, prefix='instructions'),
        }


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
