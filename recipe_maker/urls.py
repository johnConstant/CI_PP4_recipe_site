from . import views
from django.urls import path


urlpatterns = [
    path('', views.RecipeList.as_view(), name='recipes'),
    path(
        'add/', views.AddRecipe.as_view(), name='add_recipe'
        ),
    path(
        'edit/<slug>', views.EditRecipe.as_view(), name='edit_recipe'
        ),
    # path(
    #     'delete/<id>',
    #     views.CategoryDelete.as_view(),
    #     name='delete_category'
    #     ),
    path(
        '<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'
        ),

]
