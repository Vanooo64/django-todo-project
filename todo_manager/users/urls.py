from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, CustomLoginView, profile_view, CustomerCabinetView, ExecutorCabinetView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('cabinet/customer/', CustomerCabinetView.as_view(), name='cabinet_customer'),
    path('cabinet/executor/', ExecutorCabinetView.as_view(), name='cabinet_executor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
