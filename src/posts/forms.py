from django import forms

from posts.models import Post, Comment, Mark


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('sender', 'post', 'created_at')


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        exclude = ('sender', 'post', 'created_at')
