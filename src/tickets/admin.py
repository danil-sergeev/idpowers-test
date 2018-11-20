from django.contrib import admin

from tickets.models import Chat, ChatMessage


# Register your models here.


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage


class ChatAdmin(admin.ModelAdmin):
    inlines = [ChatMessageInline]

    class Meta:
        model = Chat


admin.site.register(Chat, ChatAdmin)
