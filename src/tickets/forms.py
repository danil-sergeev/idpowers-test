from django import forms

from tickets.models import Chat


class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput
    )


class ChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        exclude = ('customer', )
