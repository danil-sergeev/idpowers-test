from django.db import models

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(
        'users.Profile',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(max_length=200)
    content = models.TextField(max_length=1200)

    def __str__(self):
        return f'{self.author.username} -- {self.created_at} -- {self.title}'

    class Meta:
        ordering = ['-created_at']





