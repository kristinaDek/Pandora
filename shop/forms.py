from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, DateField, DateInput


from .models import OrderModel
from datetime import date

TIME_FORMAT = '%d.%m.%Y'

#
# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']
#         # fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        # fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class CreateOrderForm(ModelForm):
    # start_date = DateField(input_formats=[TIME_FORMAT])
    # end_date = DateField(input_formats=[TIME_FORMAT])


    class Meta:
        model = OrderModel
        fields = ['address','order_type','amount']
        exclude = ['id','user','date_of_order','price_of_order',]
