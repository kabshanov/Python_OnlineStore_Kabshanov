from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Наша кастомная view для регистрации
    path('register/', views.register, name='register'),

    # Наша кастомная view для профиля
    path('profile/', views.profile, name='profile'),

    # Встроенная view для входа
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    ), name='login'),

    # Встроенная view для выхода
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'
    ), name='logout'),
]