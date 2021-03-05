from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

# Create your views here.
from .models import *
from .forms import OrderForm
from .filters import OrderFilter

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

    #for Filter
    myFilter = OrderFilter(request.GET, queryset=orders) #take a get request to filter down from the queryset of the model
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)



#CRUD
def createOrder(request, pk):
    # OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status')) #Parent model, Child model
    customer = Customer.objects.get(id=pk)
    # formset = OrderFormSet(instance=customer)
    form = OrderForm(initial={'customer': customer}) #initial will let prefil value into the form
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/') #sending back to dashboard template

    context = {'form': form}
    # context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):

    order = Order.objects.get(id=pk) #getting data from the form
    form = OrderForm(instance=order) #this will provide exist data to the form
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST, instance=order) #sending new POST into that instance of an order
        if form.is_valid():
            form.save()
            return redirect('/') #sending back to dashboard template
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete.html', context)


