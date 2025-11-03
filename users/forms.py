from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма для создания нового пользователя.
    Использует нашу модель User.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        # Включаем поля, которые должен заполнить пользователь
        fields = ('username', 'email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    """
    Кастомная форма для редактирования профиля пользователя.
    """
    class Meta:
        model = User
        # Поля, которые пользователь может редактировать в профиле
        fields = ('username', 'email', 'first_name', 'last_name')