from django.contrib import admin

from posts.models import Post, Comment, Mark, Category
from posts.forms import PostForm


# Register your models here.

class MarkInline(admin.TabularInline):
    model = Mark


class CommentInline(admin.TabularInline):
    model = Comment


class PostInline(admin.TabularInline):
    model = Post
    form = PostForm


class PostAdminView(admin.ModelAdmin):
    inlines = [CommentInline, MarkInline]

    class Meta:
        model = Post


class CategoryAdminView(admin.ModelAdmin):
    inlines = [PostInline]

    class Meta:
        model = Category


admin.site.register(Post, PostAdminView)
admin.site.register(Category, CategoryAdminView)
