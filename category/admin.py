from django.contrib import admin
from .models import Category
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(Category)
class CategoryAdmin(SummernoteModelAdmin):

    prepopulated_fields = ({'slug': ('title',)})
    list_filter = ('created_date', 'last_modified')
    list_display = ('title', 'created_date')
    search_fields = ['title', 'description']
    summernote_fields = ('description')
