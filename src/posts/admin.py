from django.contrib import admin

from posts.models import Post, Category


# Register your models here.


class PostAdminView(admin.ModelAdmin):
    pass


class CategoryAdminView(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdminView)
admin.site.register(Category, CategoryAdminView)
