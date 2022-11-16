from django.contrib import admin

# Register your models here.

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


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):

    list_filter = ('approved', 'created_date')
    list_display = ('name', 'body', 'recipe', 'created_date')
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
