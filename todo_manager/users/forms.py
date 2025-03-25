from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.UserType.choices, label="Тип користувача")
    phone_number = forms.CharField(max_length=15, required=False, label="Номер телефону")
    profile_picture = forms.ImageField(required=False, label="Фото профілю")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "user_type", "phone_number", "profile_picture", "password1", "password2")
