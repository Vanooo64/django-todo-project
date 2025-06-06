import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from chat.models import Chat, Message  # Правильні моделі
from django.core.files.base import ContentFile
from orders.models import Order  # Для збереження файлів

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ Підключення WebSocket до кімнати чату та завантаження історії повідомлень """
        self.room_name = str(self.scope['url_route']['kwargs']['room_id'])
        self.room_group_name = f'chat_{self.room_name}'
        print(f"room_name: {self.room_name}")  # Дебаг

        # Отримання або створення чату
        self.chat = await self.get_chat()

        # Додаємо користувача в групу
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Завантаження історії повідомлень із БД
        history = await self.load_history()

        # Надсилання історії повідомлень клієнту. Ми передаємо весь список як окреме повідомлення.
        await self.send(text_data=json.dumps({
            'type': 'chat_history',
            'history': history
        }))

    async def disconnect(self, close_code):
        """ Від'єднання WebSocket від групи чату """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """ Обробка повідомлення та збереження його в базі даних """
        data = json.loads(text_data)
        message = data.get('message', '')
        file_data = data.get('file', None)  # Отримуємо файл, якщо переданий
        sender_user = self.scope.get("user")

        if sender_user and sender_user.is_authenticated:
            sender = sender_user.username
            saved_message = await self.save_message(sender_user.id, message, file_data)
        else:
            sender = "Анонім"
            saved_message = None

        # Передача повідомлення всім в групі чату
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': saved_message.text if saved_message else message,
                'sender': sender,
                'file_url': saved_message.file.url if saved_message and saved_message.file else None,
            }
        )

    async def chat_message(self, event):
        """ Відправка нового повідомлення клієнтам """
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'file_url': event.get('file_url'),
        }))

    @database_sync_to_async
    def save_message(self, sender_id, text, file_data):
        """ Збереження повідомлення та файлу в базі даних """
        sender = User.objects.get(id=sender_id)
        message = Message.objects.create(chat=self.chat, sender=sender, text=text)
        if file_data:
            file_content = ContentFile(file_data.encode('utf-8'))
            message.file.save(f"{sender.username}_{self.chat.id}.txt", file_content)
        return message

    @database_sync_to_async
    def get_chat(self):
        """ Отримання чату або створення нового, якщо він не існує """
        try:
            return Chat.objects.get(id=self.room_name)
        except Chat.DoesNotExist:
            print(f"Чат з ID {self.room_name} не існує! Перевіряємо наявність чату...")
            order = Order.objects.get(id=35)  # ❗ Замініть реальним `order_id`
            executor = User.objects.get(id=23)  # ❗ Замініть реальним `executor_id`
            existing_chat = Chat.objects.filter(order=order, executor=executor).first()
            if existing_chat:
                print(f"Чат для Order {order.id} і Executor {executor.id} вже існує!")
                return existing_chat
            return Chat.objects.create(order=order, customer=order.customer, executor=executor)

    @database_sync_to_async
    def load_history(self):
        """ Завантаження історії повідомлень для даного чату """
        messages = Message.objects.filter(chat=self.chat).order_by('timestamp')
        history = []
        for msg in messages:
            history.append({
                'sender': msg.sender.username,
                'message': msg.text,
                'file_url': msg.file.url if msg.file else None,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return history
