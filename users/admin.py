from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Profile
from users.forms import SignUpForm


# Register your models here.


class CustomProfileAdminView(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(Profile, CustomProfileAdminView)
