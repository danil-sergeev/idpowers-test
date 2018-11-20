from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

profile = get_user_model()


# class EmailBackend(ModelBackend):
#     def authenticate(self, email=None, password=None, **kwargs):
#         try:
#             user = profile.objects.get(email=email)
#         except profile.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None
#
#     def get_user(self, user_id):
#         try:
#             return profile.objects.get(pk=user_id)
#         except profile.DoesNotExist:
#             return None
