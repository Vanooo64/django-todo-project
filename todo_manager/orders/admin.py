from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
from orders.models import Order, Bid

# Спочатку скасовуємо реєстрацію
admin.site.unregister(CustomUser)

# Реєструємо з власним кастомним адміном
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email')  # Обов'язкове поле для autocomplete_fields
    ordering = ('username',)

# Реєстрація Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type_of_work', 'subject', 'executor', 'status')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

# Реєстрація Bid
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('order', 'executor', 'price', 'comment', 'created_at', 'is_selected')
    autocomplete_fields = ('order', 'executor')  # Автозаповнення потребує search_fields
