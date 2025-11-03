# store/admin.py

from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category', 'price')
    search_fields = ('name', 'description')
    ordering = ('name',)

# Мы используем TabularInline, чтобы позиции заказа
# можно было редактировать прямо со страницы Заказа.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']  # Удобно для выбора товаров по ID
    extra = 0  # Не показывать пустые формы по умолчанию

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'full_name')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username', 'full_name', 'phone')
    inlines = [OrderItemInline]  # Включаем позиции заказа

# Корзины обычно не управляются вручную, но добавим для просмотра

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]