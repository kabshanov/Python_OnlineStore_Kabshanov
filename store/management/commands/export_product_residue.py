import json
from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    """
    Кастомная management-команда для экспорта остатков товаров.
    Выгружает данные в JSON-формате в stdout (стандартный вывод).
    """
    help = 'Экспортирует остатки товаров (название и остаток) в JSON'

    def handle(self, *args, **options):
        # Получаем все продукты, но берем только нужные поля
        products = Product.objects.values('name', 'stock')

        # Преобразуем QuerySet в обычный список
        data_to_export = list(products)

        # Используем json.dumps для красивого вывода в консоль
        json_data = json.dumps(data_to_export, indent=4, ensure_ascii=False)

        # self.stdout.write - это "print" для команд Django
        self.stdout.write(json_data)

        self.stdout.write(
            self.style.SUCCESS('Экспорт остатков успешно завершен.')
        )