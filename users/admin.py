from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Импортируем нашу модель

# Регистрируем нашу модель User в админке,
# используя стандартный UserAdmin для отображения
admin.site.register(User, UserAdmin)