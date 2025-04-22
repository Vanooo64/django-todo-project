from django.contrib import admin

from django.contrib import admin
from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'customer', 'executor', 'created_at')


@admin.register(Message)
class MassageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'content', 'timestamp', 'is_read')