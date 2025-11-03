# store/models.py

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Category(models.Model) :
    """
    Модель, представляющая категорию товара.
    """
    name = models.CharField(
        max_length=255,
        verbose_name="Название категории"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )

    class Meta :
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self) :
        return self.name


class Product(models.Model) :
    """
    Модель, представляющая товар в магазине.
    """
    name = models.CharField(
        max_length=255,
        verbose_name="Название товара"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    # Поле для остатков на складе (Требование заказчика №4)
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Остаток на складе"
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    # Связь "Многие-к-Одному" с Категорией
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.PROTECT,  # Защита от удаления категории, у которой есть товары
        verbose_name="Категория"
    )

    class Meta :
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['name']

    def __str__(self) :
        return self.name


class Cart(models.Model) :
    """
    Модель корзины, связанная с пользователем.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta :
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self) :
        return f"Корзина пользователя {self.user.username}"


class CartItem(models.Model) :
    """
    Модель, представляющая товар в корзине.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )

    class Meta :
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"
        # Уникальность: один товар не может быть добавлен в одну корзину дважды
        unique_together = ('cart', 'product')

    def __str__(self) :
        return f"{self.quantity} x {self.product.name} в корзине"

    @property
    def total_item_price(self) :
        """
        Рассчитывает общую стоимость
        этой позиции корзины (цена * количество).
        """
        return self.product.price * self.quantity


class Order(models.Model) :
    """
    Модель заказа, сделанного пользователем.
    """
    STATUS_CHOICES = (
        ('pending', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Сохраняем заказ, даже если пользователь удален
        null=True,
        related_name='orders',
        verbose_name="Пользователь"
    )
    # Поля для адреса и ФИО (Требование заказчика №1)
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    address = models.CharField(max_length=1024, verbose_name="Адрес доставки")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заказа"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta :
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self) :
        return f"Заказ №{self.id} от {self.created_at.strftime('%Y-%m-%d')}"


class OrderItem(models.Model) :
    """
    Модель, представляющая товар в заказе.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,  # Не даем удалить товар, который есть в заказах
        related_name='order_items',
        verbose_name="Товар"
    )
    # Сохраняем цену на момент покупки
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )

    class Meta :
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self) :
        return f"{self.quantity} x {self.product.name}"