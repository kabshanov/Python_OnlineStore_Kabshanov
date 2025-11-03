# 1. Базовый образ Python
FROM  python:3.11-slim

# 2. Установка переменных окружения
# Гарантирует, что логи Python сразу попадают в консоль Docker
ENV PYTHONUNBUFFERED=1
# Указываем, где лежат настройки нашего проекта
ENV DJANGO_SETTINGS_MODULE=online_store_project.settings

# 3. Установка рабочего каталога в контейнере
WORKDIR /app

# 4. Установка зависимостей
# Копируем СНАЧАЛА только requirements.txt
COPY requirements.txt .
# Устанавливаем их. Этот шаг будет кэшироваться, ускоряя будущие сборки
RUN pip install -r requirements.txt

# 5. Копирование всего кода проекта в контейнер
COPY . .

# 6. Сборка статических файлов (CSS, JS админки)
# Это ПРАВИЛЬНОЕ место для этой команды
RUN python manage.py collectstatic --no-input

# 7. Открытие порта
# Сообщаем Docker, что приложение будет слушать порт 8000
EXPOSE 8000

# 8. Команда запуска по умолчанию (из задания)
# docker-compose все равно ее переопределит, но иметь ее - хорошая практика
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]