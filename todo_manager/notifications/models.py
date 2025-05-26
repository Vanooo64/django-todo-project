from django.conf import settings
from django.db import models
from orders.models import Order  # Імпортуємо модель Order з вашого додатку замовлень

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="User"
    )
    message = models.TextField(verbose_name="Message")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")  # Додаємо це поле
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Посилання")  
    is_read = models.BooleanField(default=False, verbose_name="Is Read")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Сповіщення"
        verbose_name_plural = "Сповіщення"

    def __str__(self):
        return f"Сповіщення для {self.user.username}: {self.message}"


