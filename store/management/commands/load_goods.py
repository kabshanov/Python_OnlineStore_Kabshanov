import json
from django.core.management.base import BaseCommand
from store.models import Product, Category
from django.db import transaction


class Command(BaseCommand):
    """
    """
    help = 'Загружает товары из JSON-файла в базу данных'

    def add_arguments(self, parser):
        # Добавляем обязательный аргумент - имя файла
        parser.add_argument('json_file', type=str, help='Путь к JSON-файлу с товарами')

    @transaction.atomic  # Оборачиваем в транзакцию
    def handle(self, *args, **options):
        file_path = options['json_file']

        try :
            with open(file_path, 'r', encoding='utf-8-sig') as f :
                data = json.load(f)

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Файл "{file_path}" не найден.'))
            return
        except json.JSONDecodeError as e:  # <-- Добавили 'as e'
            self.stderr.write(self.style.ERROR(f'Ошибка декодирования JSON в файле "{file_path}".'))
            self.stderr.write(self.style.ERROR(f'Причина: {e}'))  # <-- Добавили эту строку
            return

        if not isinstance(data, list):
            self.stderr.write(self.style.ERROR('JSON-файл должен содержать список (массив) объектов.'))
            return

        products_created = 0
        products_updated = 0

        for item in data:
            # Находим или создаем категорию
            category_name = item.get('category', 'Без категории')
            category, created = Category.objects.get_or_create(
                name=category_name
            )

            # Создаем или обновляем товар
            # update_or_create ищет товар по 'name'
            # Если находит - обновляет поля из 'defaults'
            # Если не находит - создает новый
            product, created = Product.objects.update_or_create(
                name=item['name'],
                defaults={
                    'description': item.get('description', ''),
                    'price': item['price'],
                    'stock': item['stock'],
                    'category': category,
                }
            )

            if created:
                products_created += 1
            else:
                products_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Загрузка завершена. '
                f'Создано: {products_created}, '
                f'Обновлено: {products_updated}.'
            )
        )