from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)  # using the form in forms.py
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')  # get the username

            # This will let create group on registration
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,  # create user associated with customer
                name=username,
            )

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        # grab the value of these fields
        username = request.POST.get('username')
        # these two are from the name= in HTML template
        password = request.POST.get('password')

        user = authenticate(request, username=username,
                            password=password)  # authenticate

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Username OR password is Incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    # allow us to grab all the order of that customer
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS: ', orders)

    context = {'orders': orders,  'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


# if user is not login, send it to the login page
@login_required(login_url='login')  # calling first
# @allowed_users(allowed_roles=['admin'])  # calling second
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders,
               'customers': customers,
               'total_customers': total_customers,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending
               }

    return render(request, 'accounts/dashboard.html', context)


# if user is not login, send it to the login page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()  # Query all the products in the database

    context = {'products': products}

    return render(request, 'accounts/products.html', context)


# if user is not login, send it to the login page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):  # make the url dynamic using pk as the param
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()  # grabing al the orders from the child subfield
    order_count = orders.count()

    # for Filter
    # take a get request to filter down from the queryset of the model
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


# CRUD
# if user is not login, send it to the login page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    # OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status')) #Parent model, Child model
    customer = Customer.objects.get(id=pk)
    # formset = OrderFormSet(instance=customer)
    # initial will let prefil value into the form
    form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # sending back to dashboard template

    context = {'form': form}
    # context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


# if user is not login, send it to the login page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)  # getting data from the form
    # this will provide exist data to the form
    form = OrderForm(instance=order)
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        # sending new POST into that instance of an order
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')  # sending back to dashboard template
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


# if user is not login, send it to the login page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete.html', context)
