from django.contrib import admin
from users.models import CustomUser

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'user_type')
    list_display_links = ('username',)

