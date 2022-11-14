from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
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
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = {
            'post': post,
            'liked': liked,
        }
        return render(request, 'category_detail.html', context)
