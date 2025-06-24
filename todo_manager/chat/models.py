from django.db import models

from users.models import CustomUser


class Chat(models.Model):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name='chats')  # Рядкове посилання
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chats_as_customer')
    executor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='chats_as_executor', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('order', 'customer') # Унікальне об'єднання для запобігання дублювання
        verbose_name = "Чат"
        verbose_name_plural = "Чати"

    def __str__(self):
        executor_username = self.executor.username if self.executor else "необраний"
        return f"Чат: {self.order.title} [{self.customer.username} ↔ {executor_username}]"



class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    comment = models.TextField(blank=True, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Повідомлення"
        verbose_name_plural = "Повідомлення"

    def __str__(self):
        return f"Від {self.sender.username} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
