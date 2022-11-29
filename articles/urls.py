from . import views
from django.urls import path


urlpatterns = [
    path('', views.ArticleList.as_view(), name='articles'),
    path('add/', views.AddArticle.as_view(), name='add_article'),
    path(
        'edit/<slug>', views.ArticleUpdate.as_view(), name='update_article'
        ),
    path(
        'delete/<id>',
        views.ArticleDelete.as_view(),
        name='delete_article'
        ),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('like/<slug:slug>', views.ArticleLike.as_view(), name='article_like'),
]