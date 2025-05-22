from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DeleteView,CreateView
from notifications.models import Notification

from .forms import OrderForm, BidForm
from .models import Order, Bid
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


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


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        form.instance._current_user = self.request.user
        return super().form_valid(form)



@login_required                                                           #доступ до цієї функції мають лише авторизовані користувачі.
def submit_bid(request, order_id):                                        #order_id передається як частина URL і визначає ідентифікатор замовлення, до якого виконавець подає пропозицію.
    order = get_object_or_404(Order, pk=order_id)                         #Отримується об'єкт замовлення з моделі Order за первинним ключем order_id, або генерується помилка 404

    # Перевірка: не дозволяти подати другу пропозицію
    if Bid.objects.filter(order=order, executor=request.user).exists():   #якщо поточний користувач вже подав пропозицію до цього замовлення, відбувається перенаправлення назад до сторінки цього замовлення.
        return redirect(order.get_absolute_url(request.user))

    if request.method == 'POST':                                            #Якщо запит — це надсилання форми (POST), то

        form = BidForm(request.POST)                                        #Створюється екземпляр форми з надісланими даними.
        if form.is_valid():                                                 #Якщо форма валідна:
            bid = form.save(commit=False)                                   #Створюється новий об’єкт Bid, але ще не зберігається в БД.
            bid.executor = request.user                                     #Задаються поля executor (поточний користувач) і order (замовлення).
            bid.order = order                                               #і order (замовлення).
            bid.save()                                                      #Пропозиція зберігається у базу.
            return redirect(order.get_absolute_url(request.user))           #Після чого відбувається перенаправлення на сторінку замовлення.

    else:
        form = BidForm()                                                    #Якщо це GET-запит, створюється порожня форма для заповнення

    return render(request, 'orders:submit_bid', {'form': form, 'order': order}) #Повертається шаблон з формою подання пропозиції.


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





    
