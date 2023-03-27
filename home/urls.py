from . import views
from django.urls import path


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path("search/", views.SearchResults.as_view(), name="search_results"),
]
