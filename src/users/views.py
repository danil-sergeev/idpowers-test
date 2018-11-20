from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.views import View
from django.db.models import Prefetch

from users.forms import SignUpForm


profile = get_user_model()


class ProfileDetailView(DetailView):
    template_name = 'profile/profile_detail.html'

    def get_queryset(self):
        queryset = profile.objects.prefetch_related(
            Prefetch('posts')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['obj'] = self.get_object(self.get_queryset())
        return context


class UpdateProfile(UpdateView):
    model = profile
    fields = ['first_name', 'last_name', 'avatar', 'skype', 'telephone']
    template_name = 'form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('users:detail', args={self.object.pk})


class CreateUser(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = '/'


class SignUpView(View):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        login_url = reverse_lazy('users:login')
        if form.is_valid():
            print(form.cleaned_data)
            user = profile.objects.create_user(
                **form.cleaned_data
            )
            print(user)
            return HttpResponseRedirect(login_url)
        return render(request, self.template_name, {'form': form})
