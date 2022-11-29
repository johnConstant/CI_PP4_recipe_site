from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Article
# from .forms import CommentForm


# Create your views here.
class ArticleList(generic.ListView):
    model = Article
    queryset = Article.objects.filter(status=1).order_by('-created_date')
    template_name = 'articles.html'
    paginate_by = 6


class ArticleDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(status=1)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.filter(approved=True).order_by('created_date')
        liked = False
        if article.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = {
            'article': article,
            'comments': comments,
            'commented': False,
            'liked': liked,
            # 'comment_form': CommentForm()
        }
        return render(request, 'article_detail.html', context)


class ArticleLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Article, slug=slug)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)

        return HttpResponseRedirect(reverse('article_detail', args=[slug]))
