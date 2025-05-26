from django.contrib import admin
from notifications.models import Notification

# Реєстрація Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'message')
    autocomplete_fields = ('order', 'user')  # Автозаповнення потребує search_fields
