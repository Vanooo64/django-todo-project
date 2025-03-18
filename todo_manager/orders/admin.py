from django.contrib import admin
from orders.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'type_of_work', 'subject', 'executor', 'status'
    list_display_links = 'id', 'title'

