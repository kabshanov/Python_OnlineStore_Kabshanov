from django import forms
from .models import Order


class AddToCartForm(forms.Form):
    """
    Форма для добавления товара в корзину.
    Содержит только поле 'quantity' (количество).
    """
    # min_value=1 означает, что нельзя добавить 0 или меньше товаров
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,  # Начальное значение в поле - 1
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class OrderForm(forms.ModelForm):
    """
    Форма для оформления заказа.
    Создана на основе модели Order, берет из нее нужные поля.
    """
    class Meta:
        model = Order
        # Мы берем только те поля, которые должен заполнить пользователь
        fields = ('full_name', 'address', 'phone')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }