from . import views
from django.urls import path


urlpatterns = [
    path('', views.RecipeList.as_view(), name='recipes'),
    path(
        'add/', views.RecipeCreate.as_view(), name='add_recipe'
        ),
    path(
        'edit/<slug:slug>', views.RecipeUpdate.as_view(), name='edit_recipe'
        ),
    path(
        'delete/<int:id>',
        views.RecipeDelete.as_view(),
        name='delete_recipe'
        ),
    path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
    path(
        '<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'
        ),

]
