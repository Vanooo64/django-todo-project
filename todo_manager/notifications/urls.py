from django.urls import path
from .views import notifications_list_customer, notifications_list_executor, notifications_list # Переконайся, що у views.py є відповідний метод

app_name = 'notifications'

urlpatterns = [
    path('', notifications_list, name='notifications_default'),  # Додаємо дефолтний маршрут
    path('executor/', notifications_list_executor, name='notifications_list_executor'),
    path('customer/', notifications_list_customer, name='notifications_list_customer'),
    # Додай інші URL-адреси для сповіщень, якщо потрібно    
]