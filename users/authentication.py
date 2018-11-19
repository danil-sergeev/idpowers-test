from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from users.models import Profile


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        #profile = get_user_model()
        try:
            user = Profile.objects.get(email__iexact=email)
            if user.check_password(password):
                return user
        except Profile.DoesNotExist:
            return None

