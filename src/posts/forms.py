from django import forms

from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('sender', 'post', 'created_at')


class MarkForm(forms.Form):
    CHOICES = tuple([(i + 1, i + 1) for i in range(5)])
    select = forms.ChoiceField(widget=forms.Select(choices=CHOICES))
