from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from recipe_maker.models import Recipe


# Create your views here.
class HomePage(View):

    def get(self, request, *args, **kwargs):
        featured_recipes = Recipe.objects.filter(featured_recipe=True) 

        context = {
            'featured_recipes': featured_recipes,
        }
        return render(request, 'home.html', context)
