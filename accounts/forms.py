from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm): #create form from the model
    class Meta:
        model = Order #Which model to use the form for
        fields = '__all__' #Go ahead and create a form with all of these fields
        # fields = ['customer', 'products']


        