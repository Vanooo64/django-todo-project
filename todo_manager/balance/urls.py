
from django.urls import path
from django.views.generic import TemplateView

from balance import views

app_name = 'balance'

urlpatterns = [
    path('withdraw/', views.WithdrawView.as_view(), name='withdraw'),
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('history/', views.TransactionHistoryView.as_view(), name='history'),
]