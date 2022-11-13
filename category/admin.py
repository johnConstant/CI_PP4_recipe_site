from django.contrib import admin
from .models import Category, Recipe, Ingredient, Instruction
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(Category)
class CategoryAdmin(SummernoteModelAdmin):

    summernote_fields = ('description')


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    prepopulated_fields = ({'slug': ('title',)})
    list_filter = ('status', 'created_date')
    list_display = ('title', 'status', 'created_date')
    search_fields = ['title', 'description', 'categories']
    summernote_fields = ('description')


@admin.register(Ingredient)
class IngredientAdmin(SummernoteModelAdmin):

    summernote_fields = ('notes')


@admin.register(Instruction)
class InstructionAdmin(SummernoteModelAdmin):

    summernote_fields = ('body')
