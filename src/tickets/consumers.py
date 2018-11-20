import asyncio
import json
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from tickets.models import Chat, ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })
        chat_pk = self.scope['url_route']['kwargs']['pk']
        chat_obj = await self.get_chat(chat_pk=chat_pk)
        print(chat_obj.admin.email)

    async def websocket_receive(self, event):
        message_text = event.get('text', None)
        if message_text is not None:
            loaded_data = json.loads(message_text)
            message = loaded_data.get('message')
            user = self.scope['user']
            response = {
                'message': message,
                'email': user.email
            }
            await self.send({
                "type": "websocket.send",
                "text": json.dumps(response)
            })

    async def websocket_disconnect(self, event):
        print(event)

    @database_sync_to_async
    def get_chat(self, chat_pk):
        chat = Chat.objects.get(pk=chat_pk)
        return chat
