from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
  """
  Кастомная модель пользователя.
  Мы используем AbstractUser, чтобы сохранить всю
  функциональность Django (логин, пароль, права),
  но в будущем сможем добавить сюда свои поля (например, телефон, адрес).
  """
  pass