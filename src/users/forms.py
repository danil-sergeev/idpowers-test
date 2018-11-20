from django import forms

from django.contrib.auth import authenticate

from django.contrib.auth.forms import UserCreationForm

from users.models import Profile


class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        print(email, password)
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("Такого пользователя не существует")

        if not user.check_password(password):
            raise forms.ValidationError('Неправильный пароль')

        if not user.is_active:
            raise forms.ValidationError('Этот аккаунт не активен')

        return super(LoginForm, self).clean(*args, **kwargs)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['password1', 'password2']
