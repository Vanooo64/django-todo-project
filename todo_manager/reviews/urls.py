from django.urls import path
from .views import reviews_view

app_name = 'reviews'

urlpatterns = [
    path('', reviews_view, name='reviews_home'),
]