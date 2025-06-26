import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from chat.models import Chat, Message
from django.core.files.base import ContentFile
from orders.models import Order

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ Підключення WebSocket до кімнати чату конкретного замовлення """
        self.order_id = str(self.scope['url_route']['kwargs']['order_id'])  # Використовуємо `order_id`
        self.room_group_name = f'chat_order_{self.order_id}'  # Унікальне ім'я групи для кожного замовлення
        self.user = self.scope.get("user")

        print(f"Підключення до чату замовлення: {self.order_id} від користувача: {self.user}")

        if not self.user.is_authenticated:
            print("Неавторизований доступ — з’єднання закрито")
            await self.close()
            return

        access_granted = await self.user_has_chat_access(self.user)
        if not access_granted:
            print(f"Доступ заборонено для користувача {self.user}")
            await self.close()
            return

        # Отримуємо або створюємо чат для конкретного `order_id`
        self.chat = await self.get_chat()

        # Додаємо користувача до групи WebSocket для конкретного замовлення
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Завантаження історії повідомлень для поточного замовлення
        history = await self.load_history()

        # Надсилаємо історію чату клієнту
        await self.send(text_data=json.dumps({
            'type': 'chat_history',
            'history': history
        }))

    async def disconnect(self, close_code):
        """ Від'єднання WebSocket від групи чату """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """ Отримання нового повідомлення та його збереження у базі """
        data = json.loads(text_data)

        message = data.get('message', '')
        comment = data.get('comment')
        price = data.get('price')

        sender_user = self.scope.get("user")

        # 🧼 Якщо comment і message однакові — не зберігай message як окреме повідомлення
        if comment and message and comment.strip() == message.strip():
            message = ''

        if sender_user and sender_user.is_authenticated:
            sender = sender_user.username

            # 🔐 Зберігаємо тільки за наявності будь-якого вмісту
            if message or comment or price:
                saved_message = await self.save_message(
                    sender_user.id,
                    message,
                    comment,
                    price
                )
            else:
                saved_message = None
        else:
            sender = "Анонім"
            saved_message = None


        # Надсилання повідомлення тільки у групу, що відповідає `order_id`
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'timestamp': saved_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'comment': comment or '',
                'price': str(price) if price else ''
            }
        )

    async def chat_message(self, event):
        """ Відправка повідомлення у WebSocket клієнтам у відповідному замовленні """
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event.get('timestamp', ''),
            'comment': event.get('comment', ''),
            'price': str(event.get('price', '')) if event.get('price') else ''
        }))

    @database_sync_to_async
    def save_message(self, sender_id, text, comment=None, price=None):
        """ Збереження повідомлення з прив’язкою до `order_id` """
        sender = User.objects.get(id=sender_id)
        order = Order.objects.get(id=self.order_id)  # Фільтрація по замовленню
        chat, created = Chat.objects.get_or_create(order=order)
        return Message.objects.create(chat=chat, sender=sender, text=text, comment=comment, price=price)

    @database_sync_to_async
    def get_chat(self):
        """ Отримання або створення чату для конкретного `order_id` """
        order = Order.objects.get(id=self.order_id)

        chat, created = Chat.objects.get_or_create (
            order=order, 
            customer=order.customer,                                
        )

        # Якщо чат створено і у замовлення вже є виконавець — встановлюємо його
        if created and order.executor:
            chat.executor = order.executor
            chat.save()

        return chat

    @database_sync_to_async
    def load_history(self):
        """ Завантаження історії повідомлень тільки для `order_id` """
        order = Order.objects.get(id=self.order_id)
        chat = Chat.objects.filter(order=order).first()
        if not chat:

            return []
        messages = Message.objects.filter(chat=chat).order_by("timestamp")
        return [{
            "sender": msg.sender.username, 
            "message": msg.text, 
            "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "comment": msg.comment, 
            "price": str(msg.price) if msg.price is not None else ''
        } for msg in messages]
    
    @database_sync_to_async
    def user_has_chat_access(self, user):
        """ Перевірка прав доступу користувача до чату замовлення """
        from orders.models import Bid
        order = Order.objects.get(id=self.order_id)

        is_customer = order.customer == user
        is_executor = order.executor == user
        has_bid = Bid.objects.filter(order=order, executor=user).exists()
       
        return is_customer or is_executor or has_bid


