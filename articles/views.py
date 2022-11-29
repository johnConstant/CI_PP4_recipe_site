import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from .models import Article, Comment
from .forms import CommentForm, ArticleForm


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
            'comment_form': CommentForm()
        }
        return render(request, 'article_detail.html', context)

    def post(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(status=1)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.filter(approved=True).order_by('created_date')
        liked = False
        if article.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
        else:
            comment_form = CommentForm()

        context = {
            'article': article,
            'comments': comments,
            'commented': True,
            'liked': liked,
            'comment_form': CommentForm()
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


class AddArticle(View):
    """
    A class view for adding a category
    """
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        context = {
            'form': form
        }
        return render(request, 'add_article.html', context)

    def post(self, request, *args, **kwargs):
        try:
            form = ArticleForm(request.POST, request.FILES)
            form.instance.slug = slugify(request.POST['title'])
            form.instance.author = request.user
            if form.is_valid():
                form.save()
                messages.success(request, "Your article has been added.")
                return redirect('articles')
        except Article.DoesNotExist:
            messages.error(request,
                           'An error occurred when adding your article.')
            return redirect('articles')


class ArticleUpdate(View):
    """
    A class view for updating an existing article
    """
    def get(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Article, slug=slug)
        form = ArticleForm(instance=article)
        context = {
            'form': form
        }
        return render(request, 'edit_article.html', context)

    def post(self, request, slug, *args, **kwargs):
        try:
            article = get_object_or_404(Article, slug=slug)
            form = ArticleForm(request.POST, request.FILES, instance=article)
            form.instance.slug = slugify(request.POST['title'])
            form.instance.last_modifed = datetime.date.today()
            if form.is_valid():
                form.save()
                messages.success(request, "Your article has been updated.")
                return redirect('articles')
        except Article.DoesNotExist:
            messages.error(request,
                           'An error occurred when updating your article.')
            return redirect('articles')


class ArticleDelete(View):
    """
    A class view for deleting an existing article
    """
    def post(self, request, id, **kwargs):
        """
        Delete a selected article
        """
        try:
            article = Article.objects.get(id=id)
            article.delete()
            messages.success(request, "Your article has been deleted.")
            return redirect('articles')
        except Article.DoesNotExist:
            messages.error(request,
                           'An error occurred when deleting your article.')
            return redirect('articles')
