from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST

from orders.models import User
from .forms import CustomUserRegistrationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматичний вхід після реєстрації
            return redirect("index")  # Перенаправлення на головну сторінку
    else:
        form = CustomUserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse_lazy("index")  # Перенаправлення на головну сторінку після входу

@require_POST
def logout_view(request):
    logout(request)  # Вихід користувача
    return redirect(reverse_lazy("index"))

@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    return render(request, 'profile/profile.html', {'user_obj': user_obj})


class CustomerCabinetView(LoginRequiredMixin, View):
    template_name = "cabinet/index.html"


    def get(self, request, *args, **kwargs):
        user = request.user

        context = {
            "user": user,
        }

        return render(request, self.template_name, context)

