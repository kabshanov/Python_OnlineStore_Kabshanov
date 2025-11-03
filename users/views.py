from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from store.models import Order # Импортируем Заказы для истории


def register(request):
    """
    Представление для регистрации нового пользователя.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            login(request, user)  # Автоматически входим в систему
            return redirect('users:profile')  # Перенаправляем в личный кабинет
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """
    Представление для личного кабинета пользователя.
    Показывает историю заказов (Требование №5).
    """
    # Получаем все заказы ТЕКУЩЕГО пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'users/profile.html', context)