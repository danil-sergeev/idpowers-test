from django import forms

from posts.models import Post, Comment, Mark


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('sender', 'post', 'content')
        widgets = {"sender": forms.HiddenInput(), "post": forms.HiddenInput()}


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('sender', 'post', 'mark')
        widgets = {"sender": forms.HiddenInput(), "post": forms.HiddenInput()}
