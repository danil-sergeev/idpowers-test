from django.contrib import admin

from posts.models import Post
# Register your models here.


class PostAdminView(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdminView)
