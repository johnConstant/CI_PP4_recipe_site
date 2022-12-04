from django.shortcuts import render, redirect
from django.views import generic, View

# Create your views here.


class Contact(View):
    """
    A class view for the contact page
    """
    def get(self, request, *args, **kwargs):
        # queryset = Category.objects.filter(status=1)
        # category = get_object_or_404(queryset, slug=slug)
        # recipes = Recipe.objects.filter(categories=category.id)

        # context = {
        #     'category': category,
        #     'recipes': recipes
        # }
        return render(request, 'contact.html')
