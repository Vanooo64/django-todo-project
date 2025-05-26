
def unread_notifications_count(request): # Контекстний процесор для підрахунку непрочитаних сповіщень
    # Перевіряємо, чи користувач автентифікований
    if request.user.is_authenticated:
        # Повертаємо словник з кількістю непрочитаних сповіщень для цього користувача
        return {
            'unread_notifications_count': request.user.notifications.filter(is_read=False).count()
        }
    # Якщо користувач не автентифікований, повертаємо 0
    return {'unread_notifications_count': 0}


