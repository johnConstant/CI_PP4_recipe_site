"""recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from category.views import PostDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('categories/', include('category.urls'), name='category_urls'),
    path('recipes/', include('recipe_maker.urls'), name='recipe_urls'),
    path('articles/', include('articles.urls'), name='article_urls'),
    path('contact/', include('contact.urls'), name='contact_urls'),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls'), name='home_urls'),
]
