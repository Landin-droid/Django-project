from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):

  class Meta:
    model = Order
    fields = ['address', 'city']
    widgets = {
      'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес доставки'}),
      'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите город'}),
    }