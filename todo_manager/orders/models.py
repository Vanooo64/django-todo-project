from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings


User = get_user_model()

# Окрема функція для отримання користувача за замовчуванням
def get_default_user():
    user = User.objects.order_by('id').first()  # Повертає першого користувача
    return user.id if user else None  # Якщо немає користувачів, повертає None

class Order(models.Model):
    class Status(models.IntegerChoices):
        NOT_PERFORMER = 0, 'Без виконавця'
        AT_WORK = 1, 'В роботі'
        COMPLETED = 2, 'Замовлення виконане'

    class WorkTypes(models.IntegerChoices):
        TUTOR = 0, "Онлайн-репетитор"
        CONTROL = 1, "Контрольна"
        TASKS = 2, "Розв'язання задач"
        COURSEWORK = 3, "Курсова"
        ESSAY = 4, "Реферат"
        ONLINE_HELP = 5, 'Онлайн-допомога'
        TEST = 6, 'Тест дистанційно'
        DIPLOM = 7, 'Диплом'
        LAB = 8, 'Лабораторна'
        DRAWING = 9, 'Креслення'
        PRACTICE_REPORT = 10, 'Звіт з практики'
        SHORT_ESSAY = 11, 'Есе'
        EXAM_ANSWERS = 12, 'Відповіді на квитки'
        PRESENTATION = 13, 'Презентація'
        TRANSLATION = 14, 'Переклад з ін. мови'
        SPEECH = 15, 'Доповідь'
        ARTICLE = 16, 'Стаття'
        COMPOSITION = 17, 'Твір'
        MASTERS_THESIS = 18, 'Магістерська дисертація'
        PHD_THESIS = 19, 'Кандидатська дисертація'
        BUSINESS_PLAN = 20, 'Бізнес-план'
        LITERATURE_REVIEW = 21, 'Підбір літератури'
        CHEAT_SHEET = 22, 'Шпаргалка'
        INFO_SEARCH = 23, 'Пошук інформації'
        NOT_STATUS = 24, 'Без предмету'

    title = models.CharField(max_length=255, verbose_name="Назва роботи")
    # slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True, verbose_name="Опис роботи")
    type_of_work = models.IntegerField(choices=WorkTypes.choices, default=WorkTypes.NOT_STATUS, verbose_name="Тип роботи")
    subject = models.CharField(max_length=255, verbose_name="Предмет")

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_orders",
        verbose_name="Замовник",
        null=True, blank=True
    )

    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="executor_orders",
        verbose_name="Виконавець"
    )

    plagiarism_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00, help_text="Рівень унікальності (%)", verbose_name="Антиплагіат"
    )
    order_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, help_text="Сума замовлення в грн", verbose_name="Сума"
    )
    file_upload = models.FileField(
        upload_to='order_files/', blank=True, null=True, help_text="Додайте файл (якщо потрібно)", verbose_name="Файл"
    )

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    def default_deadline():
        return now() + timedelta(days=7)

    deadline = models.DateTimeField(default=default_deadline, verbose_name="Термін здачі замовлення")

    status = models.IntegerField(choices=Status.choices, default=Status.NOT_PERFORMER, verbose_name="Статус")



    class Meta:
        ordering = ['-time_create']
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return f"{self.title} ({self.get_type_of_work_display()}) - {self.order_amount} грн - {self.plagiarism_percentage}%"

    def get_absolute_url(self):
        return reverse(
            "orders:detail",
            kwargs={"pk": self.pk}
        )

    def save(self, *args, **kwargs):
        if not self.customer and hasattr(self, '_current_user'):
            self.customer = self._current_user
        super().save(*args, **kwargs)