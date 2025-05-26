from django.urls import path
from .views import notifications_list, notifications_list_executor, notifications_list_customer, mark_notification_read

app_name = 'notifications'

urlpatterns = [
    path('', notifications_list, name='notifications_default'),  # Додаємо дефолтний маршрут
    path('executor/', notifications_list_executor, name='notifications_list_executor'),
    path('customer/', notifications_list_customer, name='notifications_list_customer'),
    path('read_all/', mark_notification_read, name='mark_notification_read'),  # маршрут для позначення сповіщень як прочитаних
    # Додай інші URL-адреси для сповіщень, якщо потрібно    
]