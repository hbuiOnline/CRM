from django.contrib import admin

# Register your models here.

from .models import  * # To import all the model from .models, then specify those in register

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
