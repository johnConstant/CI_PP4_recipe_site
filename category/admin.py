from django.contrib import admin
from .models import Category, Recipe, Ingredient, Instruction
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(Category)
class CategoryAdmin(SummernoteModelAdmin):

    summernote_fields = ('description')
