from django.conf import settings
from django.db import models


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='posts_by_category'
    )
    title = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(max_length=200)
    content = models.TextField(max_length=1200)

    def __str__(self):
        return f'{self.author.username} -- {self.created_at} -- {self.title}'

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Mark(models.Model):
    MARK_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='marks'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    mark = models.IntegerField(choices=MARK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def post_pk(self):
        return self.post.pk

    def __str__(self):
        return f'{self.mark} -- {self.post.title}'
