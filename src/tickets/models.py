from django.conf import settings
from django.db import models


class Chat(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='admin_in_chat')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_in_chat')
    updated = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.SET_NULL,
        null=True,
        related_name='messages'
    )
    sender = models.ForeignKey(
        'users.Profile',
        on_delete=models.CASCADE,
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
