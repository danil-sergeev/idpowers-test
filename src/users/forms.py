from django import forms

from django.contrib.auth import authenticate, get_user_model

from django.contrib.auth.forms import UserCreationForm

profile = get_user_model()


class SignUpForm(forms.Form):
    email = forms.CharField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля', required=True)
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    skype = forms.CharField(widget=forms.TextInput)
    avatar = forms.FileField(label='Аватар', required=False)
    telephone = forms.CharField(label='Номер телефона')

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        try:
            profile.objects.get(email__iexact=email)
            raise forms.ValidationError("Такой пользователь уже существует.")
        except profile.DoesNotExist:
            pass

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают. Попробуйте еще раз.")

        return super(SignUpForm, self).clean(*args, **kwargs)



#
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     class Meta:
#         model = profile
#         fields = ['password1', 'password2']
