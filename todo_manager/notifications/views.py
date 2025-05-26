from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

@login_required
def notifications_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})


@login_required
def notifications_list_executor(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/executor/notifications_list_executor.html', {'notifications': notifications})


@login_required
def notifications_list_customer(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/customer/notifications_list_customer.html', {'notifications': notifications})


def create_notification(user, message, url=None, type=None): #створення сповіщення
    """
    Create a notification for a user.
    """
    notification = Notification.objects.create(
        user=user,
        message=message,
        url=url,
        type=type
    )
    return notification


def mark_notification_read(request): #позначити сповіщення як прочитане
    request.user.notifications.filter(is_read=False).update(is_read=True) #знаходить усі сповіщення поточного користувача, які ще не прочитані (is_read=False), і встановлює для них is_read=True.
    return redirect(request.GET.get('next', request.META.get('HTTP_REFERER', 'notifications:notifications_default'))) #повертає користувача на попередню сторінку або на URL-адресу за замовчуванням, якщо next не вказано.



