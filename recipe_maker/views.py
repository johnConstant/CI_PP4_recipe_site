from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.defaultfilters import slugify
# from .forms import CategoryForm
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
