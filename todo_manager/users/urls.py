from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, CustomLoginView, profile_view, CustomerCabinetView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('cabinet/', CustomerCabinetView.as_view(), name='cabinet'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
