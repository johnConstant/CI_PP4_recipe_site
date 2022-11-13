from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Category


class CategoryList(generic.ListView):
    model = Category
    queryset = Category.objects.filter(status=1).order_by('-created_date')
    template_name = 'categories.html'
    paginate_by = 6
