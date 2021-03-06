from django.http import HttpResponse
from django.shortcuts import redirect

# A decorator is a function that take in another function as a param and add another functionality before execute the function


# This function first go into the if statement of the wrapper function to check
# if the user is authenticated, if not, it will call the loginPage function in views.py
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:  # this is a property
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):  # first throw in the role of the user
    def decorator(view_func):  # then throw in the views_function from views.py
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():  # check if user is a part of group
                # group will be set to the first group in the list
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')

        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func
