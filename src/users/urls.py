from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

from users.views import SignUpView, ProfileDetailView, UpdateProfile

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('edit/<int:pk>/', UpdateProfile.as_view(), name='edit'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='detail')
]
