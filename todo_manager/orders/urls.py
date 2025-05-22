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
    path('<int:order_id>/bid/', views.submit_bid, name='submit_bid'), #пропозиція ціни виконавцем
    path('<int:order_id>/select/<int:bid_id>/', views.select_executor, name='select_executor'), #вибір автора замовником
    path("favorites/", views.orders_where_user_executor, name="orders_where_user_executor"), # представлення списку де виконавця обрано для роботи "Вас обрано виконавцем"
    path("suggested/", views.orders_with_suggested_prices_executor, name="orders_with_suggested_prices_executor"), # представлення списку де виконавець executor "зробив ставку"
]


