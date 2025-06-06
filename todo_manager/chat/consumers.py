import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from django.contrib.auth import get_user_model

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_user = self.scope["user"]

        if sender_user.is_authenticated:
            sender = sender_user.username
            await self.save_message(sender_user.id, message)
        else:
            sender = "Анонім"

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    @database_sync_to_async
    def save_message(self, sender_id, message):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        sender = User.objects.get(id=sender_id)
        chat = Chat.objects.get(id=self.room_name)
        return Message.objects.create(chat=chat, sender=sender, content=message)
