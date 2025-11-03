from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

# Импортируем наши модели
from .models import Product, Category, Cart, CartItem

# Импортируем наши формы
from .forms import AddToCartForm, OrderForm

User = get_user_model()


class ModelTests(TestCase) :
    """
    Тестирование моделей приложения store.
    """

    def setUp(self) :
        """
        Настройка, которая выполняется перед каждым тестом.
        Создаем объекты, которые будем использовать.
        """
        self.category = Category.objects.create(name="Тестовая Категория")
        self.product = Product.objects.create(
            name="Тестовый Товар",
            category=self.category,
            price=Decimal("100.00"),
            stock=10
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )

    def test_category_str(self) :
        """
        Тестируем, что метод __str__ модели Category возвращает ее имя.
        """
        self.assertEqual(str(self.category), "Тестовая Категория")

    def test_product_str(self) :
        """
        Тестируем, что метод __str__ модели Product возвращает его имя.
        """
        self.assertEqual(str(self.product), "Тестовый Товар")

    def test_cart_item_total_price(self) :
        """
        Тестируем, что свойство total_item_price в CartItem
        правильно считает (цена * количество).
        """
        # 100.00 (цена) * 2 (количество) = 200.00
        expected_price = Decimal("200.00")
        self.assertEqual(self.cart_item.total_item_price, expected_price)


class FormTests(TestCase) :
    """
    Тестирование форм приложения store.
    """

    def test_add_to_cart_form(self) :
        """
        Тестируем форму AddToCartForm.
        """
        # 1. Валидные данные (количество > 0)
        form_valid = AddToCartForm(data={'quantity' : 5})
        self.assertTrue(form_valid.is_valid())

        # 2. Невалидные данные (количество = 0)
        form_invalid_zero = AddToCartForm(data={'quantity' : 0})
        self.assertFalse(form_invalid_zero.is_valid())

        # 3. Невалидные данные (нет данных)
        form_invalid_empty = AddToCartForm(data={})
        self.assertFalse(form_invalid_empty.is_valid())

    def test_order_form(self) :
        """
        Тестируем форму OrderForm.
        """
        # 1. Валидные данные (все поля заполнены)
        form_data = {
            'full_name' : 'Тест Тестов',
            'address' : 'г. Тест, ул. Тестовая, 1',
            'phone' : '+1234567890'
        }
        form_valid = OrderForm(data=form_data)
        self.assertTrue(form_valid.is_valid())

        # 2. Невалидные данные (пропущено обязательное поле 'full_name')
        form_data_invalid = {
            'address' : 'г. Тест, ул. Тестовая, 1',
            'phone' : '+1234567890'
        }
        form_invalid = OrderForm(data=form_data_invalid)
        self.assertFalse(form_invalid.is_valid())


class ViewTests(TestCase) :
    """
    Тестирование представлений (views) приложения store.
    """

    def setUp(self) :
        """
        Настройка для тестов представлений.
        """
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name="Категория")
        self.product = Product.objects.create(
            name="Продукт для Теста Views",
            category=self.category,
            price=50,
            stock=5
        )
        # URL'ы, которые мы будем проверять
        self.product_list_url = reverse('store:product_list')
        self.product_detail_url = reverse('store:product_detail', args=[self.product.pk])
        self.cart_detail_url = reverse('store:cart_detail')
        self.create_order_url = reverse('store:create_order')

    def test_product_list_view(self) :
        """
        Тестируем, что страница каталога (product_list)
        1. Открывается (статус 200).
        2. Содержит название нашего продукта.
        """
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Продукт для Теста Views")

    def test_product_detail_view(self) :
        """
        Тестируем, что страница товара (product_detail)
        1. Открывается (статус 200).
        2. Содержит название и цену продукта.
        """
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Продукт для Теста Views")
        self.assertContains(response, "50")  # Проверка цены

    def test_cart_access_redirects_unauthenticated(self) :
        """
        Тестируем, что страницы корзины и заказа
        перенаправляют неавторизованного пользователя
        на страницу входа.
        """
        # 1. Проверяем корзину
        response_cart = self.client.get(self.cart_detail_url)
        self.assertEqual(response_cart.status_code, 302)  # 302 - это редирект
        self.assertRedirects(response_cart, f"{reverse('users:login')}?next={self.cart_detail_url}")

        # 2. Проверяем оформление заказа
        response_order = self.client.get(self.create_order_url)
        self.assertEqual(response_order.status_code, 302)
        self.assertRedirects(response_order, f"{reverse('users:login')}?next={self.create_order_url}")

    def test_cart_access_authenticated(self) :
        """
        Тестируем, что авторизованный пользователь
        может получить доступ к своей корзине.
        """
        # "Входим" в систему под нашим тестовым пользователем
        self.client.login(username='testuser', password='password123')

        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ваша корзина")