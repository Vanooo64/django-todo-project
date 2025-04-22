from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DeleteView,CreateView

from .forms import OrderForm
from .models import Order


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


class OrderShowViewExecutor(DeleteView):
    model = Order
    template_name = 'orders/executor/show_detail_executor.html'


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        form.instance._current_user = self.request.user
        return super().form_valid(form)








    
