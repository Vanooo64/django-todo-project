from datetime import datetime
from orders.models import Order


def global_variables(request):
    return {
        'timestamp': datetime.now().timestamp()
    }


def new_orders_count(request): # Контекстний процесор для підрахунку нових замовлень
    # Перевіряємо, чи користувач автентифікований і чи є у нього роль виконавця
    if request.user.is_authenticated and hasattr(request.user, 'user_type') and request.user.user_type == 'executor':
        return {
            'new_orders_count': Order.objects.filter(executor__isnull=True).count()
        }
    return {'new_orders_count': 0}