from django.urls import path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/order/<int:order_id>/", ChatConsumer.as_asgi()),  # Тепер чати фільтруються за `order_id`
]
