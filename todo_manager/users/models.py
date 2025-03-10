from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Замовник"
        EXECUTOR = "executor", "Виконавець"

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.CUSTOMER,
        verbose_name="Тип користувача"
    )
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Номер телефону")
    profile_picture = models.ImageField(upload_to='user_profiles/', blank=True, null=True, verbose_name="Фото профілю")
    bio = models.TextField(blank=True, verbose_name="Опис профілю")

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"