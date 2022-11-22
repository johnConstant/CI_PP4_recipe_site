from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.db.models import Q
from recipe_maker.models import Recipe


# Create your views here.
class HomePage(View):

    def get(self, request, *args, **kwargs):
        featured_recipes = Recipe.objects.filter(featured_recipe=True).order_by('last_modified')[:5]
        most_popular = Recipe.objects.all().order_by('likes')[:3]

        context = {
            'featured_recipes': featured_recipes,
            'most_popular': most_popular
        }
        return render(request, 'home.html', context)


class SearchResults(generic.ListView):
    model = Recipe
    template_name = "search_results.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Recipe.objects.filter(title__contains=query)
        #     Q(title__contains=query) | Q(categories__contains=query)
        # )
        return object_list
