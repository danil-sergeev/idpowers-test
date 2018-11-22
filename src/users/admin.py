from django.contrib import admin

from users.models import Profile


# Register your models here.


class CustomProfileAdminView(admin.ModelAdmin):
    pass


admin.site.register(Profile, CustomProfileAdminView)
