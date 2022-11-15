from . import views
from django.urls import path


urlpatterns = [
    path('', views.CategoryList.as_view(), name='categories'),
    path(
        '<slug:slug>/', views.CategoryDetail.as_view(), name='category_detail'
        ),
    path(
        'add/', views.CategoryAdd.as_view(), name='add_category'
        ),

]
