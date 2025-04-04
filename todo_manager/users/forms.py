from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    # Поле для типу користувача можна зробити невидимим для користувача
    # і призначати його через URL-параметр на сервері
    user_type = forms.ChoiceField(
        choices=CustomUser.UserType.choices,
        label="Тип користувача",
        widget=forms.HiddenInput()  # Сховаємо це поле
    )
    phone_number = forms.CharField(max_length=15, required=False, label="Номер телефону")
    profile_picture = forms.ImageField(required=False, label="Фото профілю")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "user_type", "phone_number", "profile_picture", "password1", "password2")

    def __init__(self, *args, **kwargs):
        # Якщо передано значення 'role' в kwargs, ми призначаємо його в user_type
        role = kwargs.pop('role', 'customer')  # За замовчуванням роль 'customer'
        super().__init__(*args, **kwargs)

        # Призначаємо тип користувача на основі параметра 'role'
        self.fields['user_type'].initial = role
        self.fields['user_type'].widget.attrs[
            'readonly'] = True  # Робимо поле тільки для читання, щоб не змінювати його на формі

    def save(self, commit=True):
        user = super().save(commit=False)

        # Встановлюємо тип користувача, якщо він ще не був змінений
        if self.cleaned_data.get('user_type'):
            user.user_type = self.cleaned_data['user_type']

        if commit:
            user.save()
        return user
