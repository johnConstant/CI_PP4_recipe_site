import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.defaultfilters import slugify
from .forms import CategoryForm
from .models import Category
from recipe_maker.models import Recipe


class CategoryList(generic.ListView):
    """
    A class view for getting all categories
    """
    model = Category
    queryset = Category.objects.filter(status=1).order_by('-created_date')
    template_name = 'categories.html'
    paginate_by = 10


class CategoryDetail(View):
    """
    A class view for getting a specific category
    """
    def get(self, request, slug, *args, **kwargs):
        queryset = Category.objects.filter(status=1)
        category = get_object_or_404(queryset, slug=slug)
        recipes = Recipe.objects.filter(categories=category.id)

        context = {
            'category': category,
            'recipes': recipes
        }
        return render(request, 'category_detail.html', context)


class CategoryAdd(View):
    """
    A class view for adding a category
    """
    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        context = {
            'form': form
        }
        return render(request, 'add_category.html', context)

    def post(self, request, *args, **kwargs):
        try:
            form = CategoryForm(request.POST, request.FILES)
            form.instance.slug = slugify(request.POST['title'])
            if form.is_valid():
                form.save()
                messages.success(request, "Your category has been added.")
                return redirect('categories')
        except Category.DoesNotExist:
            messages.error(request,
                           'An error occurred when adding your category.')
            return redirect('categories')


class CategoryUpdate(View):
    """
    A class view for updating an existing category
    """
    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        form = CategoryForm(instance=category)
        context = {
            'form': form
        }
        return render(request, 'edit_category.html', context)

    def post(self, request, slug, *args, **kwargs):
        try:
            category = get_object_or_404(Category, slug=slug)
            form = CategoryForm(request.POST, request.FILES, instance=category)
            form.instance.slug = slugify(request.POST['title'])
            form.instance.last_modifed = datetime.date.today()
            if form.is_valid():
                form.save()
                messages.success(request, "Your category has been updated.")
                return redirect('categories')
        except Category.DoesNotExist:
            messages.error(request,
                           'An error occurred when updating your category.')
            return redirect('categories')


class CategoryDelete(View):
    """
    A class view for deleting an existing category
    """
    def post(self, request, id, **kwargs):
        """
        Delete a selected category
        """
        try:
            category = Category.objects.get(id=id)
            category.delete()
            messages.success(request, "Your category has been deleted.")
            return redirect('categories')
        except Category.DoesNotExist:
            messages.error(request,
                           'An error occurred when deleting your category.')
            return redirect('categories')
