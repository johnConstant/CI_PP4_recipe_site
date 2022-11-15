from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
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
        if form.is_valid():
            form.save()
            return redirect('categories')
        else:
            return redirect('categories')
