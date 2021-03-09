from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User  # import User model
from .models import *


# Customer can update their own information except the username
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class OrderForm(ModelForm):  # create form from the model
    class Meta:
        model = Order  # Which model to use the form for
        fields = '__all__'  # Go ahead and create a form with all of these fields
        # fields = ['customer', 'products']


# inherited the UserCreationForm, replicate it customize the field
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # this will give the form of only these fields
        fields = ['username', 'email', 'password1', 'password2']
