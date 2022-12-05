from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    """
    A class view creating the Article form
    """
    class Meta:
        model = Article
        fields = [
            'title', 'topic', 'excerpt', 'content', 'featured_image', 'status'
            ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
