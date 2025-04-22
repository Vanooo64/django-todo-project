from django.db import models

from orders.models import Order
from users.models import CustomUser


# Create your models here.
class Chat(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='chats')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chats_as_customer')
    executor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chats_as_executor')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('order', 'executor')
        verbose_name = "Чат"
        verbose_name_plural = "Чати"

    def __str__(self):
        return f"Чат: {self.order.title} [{self.customer.username} ↔ {self.executor.username}]"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Повідомлення"
        verbose_name_plural = "Повідомлення"

    def __str__(self):
        return f"Від {self.sender.username} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
