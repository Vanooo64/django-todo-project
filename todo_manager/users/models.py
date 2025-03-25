from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


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

    # Нові поля
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Баланс")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name="Рейтинг")
    completed_orders = models.PositiveIntegerField(default=0, verbose_name="Виконані замовлення")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    is_verified = models.BooleanField(default=False, verbose_name="Підтверджений акаунт")
    country = models.CharField(max_length=100, blank=True, verbose_name="Країна")
    city = models.CharField(max_length=100, blank=True, verbose_name="Місто")
    registration_date = models.DateTimeField(default=now, verbose_name="Дата реєстрації")

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()}) - Баланс: {self.balance} грн - Рейтинг: {self.rating}"
