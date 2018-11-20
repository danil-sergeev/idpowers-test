import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from tickets.models import Chat, ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        chat_pk = self.scope['url_route']['kwargs']['pk']
        chat_obj = await self.get_chat(chat_pk=chat_pk)

        chat_room = f"chat_{chat_pk}"
        self.chat_room = chat_room
        self.chat_obj = chat_obj

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

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
            await self.create_message(sender=user, message=message)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(response)
                }
            )

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    async def websocket_disconnect(self, event):
        print(event)

    @database_sync_to_async
    def get_chat(self, chat_pk):
        chat = Chat.objects.get(pk=chat_pk)
        return chat

    @database_sync_to_async
    def create_message(self, sender, message):
        chat_obj = self.chat_obj
        return ChatMessage.objects.create(chat=chat_obj, sender=sender, message=message)
