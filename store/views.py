from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import AddToCartForm, OrderForm


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
    product = get_object_or_404(Product, pk=pk)
    add_to_cart_form = AddToCartForm()  # <-- 2. Создаем экземпляр формы

    context = {
        'product' : product,
        'add_to_cart_form' : add_to_cart_form,  # <-- 3. Добавляем в context
    }
    return render(request, 'store/product_detail.html', context)


@login_required
def add_to_cart(request, pk) :
    """
    Добавление товара в корзину.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST' :
        form = AddToCartForm(request.POST)
        if form.is_valid() :
            quantity = form.cleaned_data['quantity']

            # --- ПРОВЕРКА ОСТАТКОВ (Требование №4) ---
            if quantity > product.stock :
                messages.error(request, f"На складе недостаточно товара (осталось: {product.stock})")
                return redirect('store:product_detail', pk=pk)

            # Получаем или создаем корзину для пользователя
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Получаем или создаем позицию в корзине
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity' : 0}
            )

            # Проверяем, не превысит ли новое кол-во остатки
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock :
                messages.error(request, f"Нельзя добавить больше, чем на складе (осталось: {product.stock})")
                return redirect('store:product_detail', pk=pk)

            # Обновляем количество и сохраняем
            cart_item.quantity = new_quantity
            cart_item.save()

            messages.success(request, f"Товар '{product.name}' добавлен в корзину.")
            return redirect('store:cart_detail')

    # Если GET-запрос, просто вернем на страницу товара
    return redirect('store:product_detail', pk=pk)


@login_required
def cart_detail(request) :
    """
    Отображение содержимого корзины.
    """
    try :
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        # Считаем общую стоимость
        total_price = sum(item.total_item_price for item in cart_items)
    except Cart.DoesNotExist :
        cart_items = []
        total_price = 0

    context = {
        'cart_items' : cart_items,
        'total_price' : total_price,
    }
    return render(request, 'store/cart_detail.html', context)


@login_required
@transaction.atomic  # Гарантирует, что все операции с БД выполнятся, или ни одной
def create_order(request) :
    """
    Оформление заказа.
    """
    try :
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        if not cart_items :
            # Если корзина пуста, отправляем обратно
            messages.error(request, "Ваша корзина пуста.")
            return redirect('store:cart_detail')
    except Cart.DoesNotExist :
        messages.error(request, "У вас нет корзины.")
        return redirect('store:product_list')

    if request.method == 'POST' :
        form = OrderForm(request.POST)
        if form.is_valid() :
            # Создаем заказ, но пока не сохраняем в БД (commit=False)
            order = form.save(commit=False)
            order.user = request.user
            order.save()  # Теперь сохраняем, чтобы получить ID заказа

            # --- ПРОВЕРКА ОСТАТКОВ (Финальная) ---
            for item in cart_items :
                product = item.product
                if item.quantity > product.stock :
                    # Если товара не хватает, откатываем транзакцию
                    messages.error(request, f"Товара '{product.name}' не хватает на складе.")
                    # @transaction.atomic отменит создание 'order'
                    return redirect('store:cart_detail')

            # Если все в порядке, создаем позиции заказа и списываем остатки
            for item in cart_items :
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                # Уменьшаем остатки на складе
                item.product.stock -= item.quantity
                item.product.save()

            # Очищаем корзину
            cart.items.all().delete()

            messages.success(request, "Ваш заказ успешно оформлен!")
            # Перенаправляем на страницу "Спасибо" (создадим в Шаге 4)
            return redirect('store:order_success')
    else :
        # GET-запрос: просто показываем форму
        form = OrderForm()

    context = {
        'form' : form,
        'cart_items' : cart_items,
    }
    return render(request, 'store/create_order.html', context)


def order_success(request) :
    """
    Страница "Спасибо за заказ".
    """
    return render(request, 'store/order_success.html')