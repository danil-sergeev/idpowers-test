from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

from users.views import CreateUser, signup_view

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('sign-up/', signup_view, name='sign-up')
]
