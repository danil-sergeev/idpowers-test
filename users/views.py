from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q
from django import forms
from django.views.generic import CreateView

from users.models import Profile
from users.forms import SignUpForm, LoginForm


# Create your views here.

class CreateUser(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = '/'


def signup_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = request.POST['password1']
        try:
            Profile.objects.get(email__iexact=email)
            raise forms.ValidationError("Username with that email or password already exists")
        except Profile.DoesNotExist:
            profile_obj = Profile.objects.create_user(email=email, password=password)
            user = authenticate(email=profile_obj.email, password=profile_obj.password)
            print(user)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {"form": form})
