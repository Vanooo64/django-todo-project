from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.views import View
from django.views.decorators.http import require_POST

from orders.models import User
from .forms import CustomUserRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


User = get_user_model()


def register(request):
    # Отримуємо параметр 'role' з URL, значення за замовчуванням - 'customer'
    role = request.GET.get('role', 'customer')

    # Перевіряємо, чи є правильний параметр 'role'
    if role not in ['customer', 'executor']:
        return HttpResponseBadRequest("Невірний параметр ролі.")

    form = CustomUserRegistrationForm()  # Ініціалізуємо порожню форму

    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Призначаємо роль користувачеві
            if role == 'customer':
                user.user_type = User.UserType.CUSTOMER
                redirect_url = "orders:create"  # Сторінка створення замовлення
            elif role == 'executor':
                user.user_type = User.UserType.EXECUTOR
                redirect_url = "users:cabinet_executor"  # Кабінет виконавця

            user.save()  # Зберігаємо користувача з вибраною роллю

            # Автоматичний вхід після реєстрації
            login(request, user)

            return redirect(redirect_url)  # Перенаправлення користувача

    # Вибір шаблону в залежності від ролі
    template_name = f"registration/register_{role}.html"

    return render(request, template_name, {"form": form})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.user_type == User.UserType.CUSTOMER:
            return reverse_lazy("users:cabinet_customer")
        elif user.user_type == User.UserType.EXECUTOR:
            return reverse_lazy("users:cabinet_executor")
        return reverse_lazy("index")  # Якщо ролі немає, повертає на головну


@require_POST
def logout_view(request):
    logout(request)  # Вихід користувача
    return redirect(reverse_lazy("index"))

@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    return render(request, 'profile/profile.html', {'user_obj': user_obj})


class CustomerCabinetView(LoginRequiredMixin, View):
    template_name = "cabinet/customer/base_customer_cabinet.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        context = {
            "user": user,
        }

        return render(request, self.template_name, context)


class ExecutorCabinetView(LoginRequiredMixin, View):
    template_name = "cabinet/executor/base_executor_cabinet.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        context = {
            "user": user,
        }

        return render(request, self.template_name, context)

