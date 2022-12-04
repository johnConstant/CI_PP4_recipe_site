from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.db.models import Q
from recipe_maker.models import Recipe
from category.models import Category
from articles.models import Article


# Create your views here.
class HomePage(View):
    """
    A class for the Home page view
    """
    def get(self, request, *args, **kwargs):
        featured_recipes = (
            Recipe.objects.filter(featured_recipe=True)
            .order_by('last_modified')[:5]
        )
        most_popular = Recipe.objects.all().order_by('likes')[:3]
        most_recent = Category.objects.all().order_by('-created_date')[:6]
        articles = Article.objects.all().order_by('-created_date')[:2]

        context = {
            'featured_recipes': featured_recipes,
            'most_popular': most_popular,
            'most_recent': most_recent,
            'articles': articles
        }
        return render(request, 'home.html', context)


class SearchResults(View):
    """
    A class for the Search results page view
    """
    # model = Recipe
    # template_name = "search_results.html"

    def get(self, request, *args, **kwargs): 
        query = self.request.GET.get("q")
        recipe_list = Recipe.objects.filter(title__contains=query)
        category_list = Category.objects.filter(title__contains=query)
        article_list = Article.objects.filter(title__contains=query)

        context = {
            'recipe_list': recipe_list,
            'category_list': category_list,
            'article_list': article_list
        }
        print(context)
        return render(request, 'search_results.html', context)
