from . import views
from django.urls import path


urlpatterns = [
    path('categories', views.CategoryList.as_view(), name='categories'),
    path(
        '<slug:slug>/', views.CategoryDetail.as_view(), name='category_detail'
        ),
    path(
        'categories/add/', views.CategoryAdd.as_view(), name='add_category'
        ),

]
