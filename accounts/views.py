from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import *

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()


    context = { 'orders': orders, 
                'customers': customers, 
                'total_customers': total_customers, 
                'total_orders': total_orders, 
                'delivered': delivered, 
                'pending': pending
            }

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all() #Query all the products in the database

    context = {'products': products}

    return render(request, 'accounts/products.html', context)

def customer(request, pk): #make the url dynamic using pk as the param
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all() #grabing al the orders from the child subfield
    order_count = orders.count()

    context = {'customer': customer, 'orders': orders, 'order_count': order_count}
    return render(request, 'accounts/customer.html', context)



