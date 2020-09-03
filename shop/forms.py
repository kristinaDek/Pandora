from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, DateField, DateInput


from .models import OrderModel





class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']



class CreateOrderForm(ModelForm):

    class Meta:
        model = OrderModel
        fields = ['address','order_type','amount']
        exclude = ['id','user','date_of_order','price_of_order',]
