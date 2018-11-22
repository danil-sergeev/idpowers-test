from django import forms
from django.contrib.auth import get_user_model

from tickets.models import Chat

profile = get_user_model()


class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput
    )


class ChatCreateForm(forms.ModelForm):
    queryset = profile.objects.all().filter(is_superuser=True)
    admin = forms.ModelChoiceField(queryset=queryset, empty_label="Выберите администратора")

    class Meta:
        model = Chat
        exclude = ('customer', 'admin')
