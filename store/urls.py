from django.urls import path
from . import views  # Импортируем 'views' из текущей папки

# 'app_name' позволяет нам использовать 'store:product_list' в шаблонах
app_name = 'store'

urlpatterns = [
    # http://127.0.0.1:8000/products/
    path('products/', views.product_list, name='product_list'),

    # http://127.0.0.1:8000/products/1/ (где 1 - это 'pk')
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
]