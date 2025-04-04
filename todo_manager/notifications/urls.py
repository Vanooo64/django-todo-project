from django.urls import path
from .views import notifications_view  # Переконайся, що у views.py є відповідний метод

app_name = 'notifications'

urlpatterns = [
    path('', notifications_view, name='notifications_home'),
]