from django.urls import path
from django.views.generic import TemplateView

from . import views
app_name = 'orders'

urlpatterns = [
    path("", views.OrderListView.as_view(), name='index'),
    path("<int:pk>/", views.OrderShowView.as_view(), name='detail'),
    path("list/", views.OrderListIndexView.as_view(), name='list'),
    path("not_performer/", views.OrderListNotPerformerView.as_view(), name='not_performer'),
    path("create/", views.OrderCreateView.as_view(), name='create'),
]
