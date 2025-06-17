from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DeleteView,CreateView
from notifications.models import Notification

from .forms import OrderForm, BidForm
from .models import Order, Bid
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.utils import timezone
from datetime import timedelta


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        form.instance._current_user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url(self.request.user)



class OrderListCustomerView(LoginRequiredMixin, ListView): #список замовлень для замовника
    model = Order
    template_name = 'orders/components/orders_customer_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['customer_orders'] = Order.objects.filter(customer=user)
        return context


class OrderListExecutorView(LoginRequiredMixin, ListView): #список замовлень для виконавця
    model = Order
    template_name = 'orders/orders_executor_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(executor=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['executor_orders'] = Order.objects.filter(executor=user)
        return context


class OrderShowViewCustomer(DeleteView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/customer/show_detail_customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bids'] = Bid.objects.filter(order=self.object).select_related('executor')
        return context



class OrderShowViewExecutor(DeleteView):
    model = Order
    template_name = 'orders/executor/show_detail_executor.html'



@login_required                                                           #доступ до цієї функції мають лише авторизовані користувачі.
def submit_bid(request, order_id):                                        #order_id передається як частина URL і визначає ідентифікатор замовлення, до якого виконавець подає пропозицію.
    order = get_object_or_404(Order, pk=order_id)                         #Отримується об'єкт замовлення з моделі Order за первинним ключем order_id, або генерується помилка 404
    existing_bid = Bid.objects.filter(order=order, executor=request.user).first()  #Перевіряється, чи вже існує пропозиція від поточного користувача для цього замовлення. Якщо така пропозиція існує, вона зберігається в змінній executing_bid.
    
    if request.method == 'POST':  #Якщо запит є POST і вже існує пропозиція від поточного користувача, то:
        form = BidForm(request.POST, instance=existing_bid)  #Створюється форма з надісланими даними, яка заповнюється даними існуючої пропозиції.
        if form.is_valid():  #Якщо форма валідна:
            bid = form.save(commit=False)  #Зберігається об'єкт Bid, але ще не зберігається в базі даних.
            bid.executor = request.user  #Задається поле executor (поточний користувач).
            bid.order = order  #Задається поле order (замовлення).
            bid.save()  #Пропозиція зберігається в базу даних.

            if bid.comment or bid.price:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'chat_order_{order.id}',
                    {
                        'type': 'chat_message',
                        'message': f"💰 Пропозиція: {bid.price} грн\n📝 Коментар: {bid.comment or '(без коментаря)'}",
                        'sender': request.user.username,
                    }   
                ) #Якщо є коментар або ціна, то відправляється повідомлення в групу чату замовлення з інформацією про пропозицію.
            
            return redirect(order.get_absolute_url(request.user))  #Після чого відбувається перенаправлення на сторінку замовлення.
    else:  #Якщо це GET-запит або якщо не існує пропозиції від поточного користувача:
        form = BidForm(instance=existing_bid)  #Створюється форма з даними існуючої пропозиції, якщо вона є, або порожня форма для заповнення.
    # Повертається шаблон з формою подання пропозиції.



    return render(request, 'orders:submit_bid', {
        'form': form, 
        'order': order,
        'existing_bid': existing_bid, 
    }) #Повертається шаблон з формою подання пропозиції.


@login_required
def select_executor(request, order_id, bid_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    bid = get_object_or_404(Bid, pk=bid_id, order=order)

    order.executor = bid.executor
    order.status = Order.Status.AT_WORK
    order.order_amount = bid.price
    order.save()

    bid.is_selected = True
    bid.save()

    # Опціонально: деактивувати інші пропозиції
    order.bids.exclude(pk=bid.pk).update(is_selected=False)

    # Створити сповіщення для виконавця
    Notification.objects.create(
        user=bid.executor,
        message=f"Вас обрано виконавцем для замовлення '{order.title}'",
        order=order
    )

    return redirect(order.get_absolute_url(request.user))


@login_required
def orders_where_user_executor(request): # представлення для замовлень в яких executor "Вас обрано виконавцем"
    orders = Order.objects.filter(executor=request.user)
    return render(request,'orders/executor/orders_where_user_executor.html', {"orders": orders})


@login_required
def orders_with_suggested_prices_executor(request): # представлення для замовлень в яких executor "зробив ставку"
    # Знаходимо всі Bid цього користувача
    bids = Bid.objects.filter(executor=request.user).select_related('order')
    # Витягуємо id замовлень, де є ставки цього користувача
    order_ids = bids.values_list('order_id', flat=True).distinct()
    # Фільтруємо замовлення по цим id
    orders = Order.objects.filter(id__in=order_ids)

    return render(request,'orders/executor/orders_with_suggested_prices_executor.html', {"orders": orders})


@login_required
def search_new_orders_executor(request):  # представлення списку з новими замовленнями де можна зробити ставку (за останні 3 дні)
    three_days_ago = timezone.now() - timedelta(days=3)
    orders = Order.objects.filter(
        status=Order.Status.NOT_PERFORMER,
        executor__isnull=True,
        time_create__gte=three_days_ago
    )
    return render(request, 'orders/executor/search_new_orders_executor.html', {'orders': orders})
