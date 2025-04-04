from django.urls import path
from .views import chat_view  # Переконайся, що у views.py є відповідний метод

app_name = 'chat'

urlpatterns = [
    path('', chat_view, name='chat_home'),
]