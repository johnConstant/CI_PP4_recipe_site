from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from .forms import CategoryForm
from .models import Category


class CategoryList(generic.ListView):
    model = Category
    queryset = Category.objects.filter(status=1).order_by('-created_date')
    template_name = 'categories.html'
    paginate_by = 6


class CategoryDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Category.objects.filter(status=1)
        category = get_object_or_404(queryset, slug=slug)

        context = {
            'category': category,
        }
        return render(request, 'category_detail.html', context)


class CategoryAdd(View):

    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        context = {
            'form': form
        }
        return render(request, 'add_category.html', context)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        form.instance.slug = slugify(request.POST['title'])
        if form.is_valid():
            form.save()
            return redirect('categories')


class CategoryUpdate(View):

    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        form = CategoryForm(instance=category)
        context = {
            'form': form
        }
        return render(request, 'edit_category.html', context)

    def post(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')


class CategoryDelete(View):

    def post(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return redirect('categories')
