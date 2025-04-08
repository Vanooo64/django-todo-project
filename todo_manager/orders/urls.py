from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'orders'

urlpatterns = [
    path('customer/', views.OrderListCustomerView.as_view(), name='customer'),
    path('executor/', views.OrderListExecutorView.as_view(), name='executor'),
    path("customer/<int:pk>/", views.OrderShowViewCustomer.as_view(), name='detail_order_customer'),
    path("executor/<int:pk>/", views.OrderShowViewExecutor.as_view(), name='detail_order_executor'),
    path("create/", views.OrderCreateView.as_view(), name='create'),

]
