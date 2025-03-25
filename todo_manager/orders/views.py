from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DeleteView,CreateView

from .forms import OrderForm
from .models import Order


class OrderListIndexView(ListView):
    template_name = 'orders/order_item_list.html'
    queryset = Order.objects.all()[:2]


class OrderListView(ListView):
    model = Order
    template_name = 'orders/index.html'


class OrderListNotPerformerView(ListView):
    template_name = 'orders/not_performer.html'
    queryset = Order.objects.filter(status=Order.Status.NOT_PERFORMER).all()


class OrderShowView(DeleteView):
    model = Order
    template_name = 'orders/show_detail.html'


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        form.instance._current_user = self.request.user
        return super().form_valid(form)


    
