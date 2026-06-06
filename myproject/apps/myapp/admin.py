from django.contrib import admin
from .models import Article, Category, Comment, Favorite


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'created_at',
        'views_count',
        'is_published'
    )
    list_filter = (
        'is_published',
        'created_at',
        'category'
    )
    search_fields = (
        'title',
        'content'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'article',
        'author',
        'created_at'
    )
    list_filter = ('created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'article',
        'created_at'
    )