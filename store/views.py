from django.shortcuts import render, get_object_or_404
from .models import Product


def product_list(request):
    """
    Представление для отображения списка всех товаров.
    """
    # Получаем все объекты (товары) из базы данных
    products = Product.objects.all()

    # Передаем товары в шаблон 'store/product_list.html'
    context = {
        'products': products
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, pk):
    """
    Представление для отображения детальной информации о товаре.
    'pk' (Primary Key) - это уникальный ID товара.
    """
    # get_object_or_404 - стандартный способ получить объект.
    # Он автоматически вернет "Страница не найдена" (404),
    # если товар с таким 'pk' не будет найден.
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)