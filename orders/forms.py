from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Иван'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Иванов'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Россия'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Москва'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ул. Мира, дом 6'}))
    postcode = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '432027'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'country', 'city', 'address', 'postcode', 'email', )