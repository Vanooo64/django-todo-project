from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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