from django.contrib import admin
from .models import Contact
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(Contact)
class ContactAdmin(SummernoteModelAdmin):

    list_filter = ('created_date',)
    list_display = ('name', 'message')
    search_fields = ['name', 'message']
    summernote_fields = ('message')
