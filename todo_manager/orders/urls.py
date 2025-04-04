from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'orders'

urlpatterns = [
    path('customer/', views.OrderListCustomerView.as_view(), name='customer'),
    path('executor/', views.OrderListExecutorView.as_view(), name='executor'),
    path("<int:pk>/", views.OrderShowView.as_view(), name='detail'),
    path("create/", views.OrderCreateView.as_view(), name='create'),

]
