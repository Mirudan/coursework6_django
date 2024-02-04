from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_on', 'is_published')
    search_fields = ('title', 'created_on',)
    list_filter = ('is_published',)