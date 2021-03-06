from django.urls import path
from . import views

urlpatterns = [

    # Login system
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),



    # using name to reference for dynamic routing
    path('', views.home, name="home"),
    path('user/', views.userPage, name='user-page'),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>', views.customer, name="customer"),

    path('create_order/<str:pk>', views.createOrder,
         name="create_order"),  # getting id of the customer
    path('update_order/<str:pk>', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>', views.deleteOrder, name="delete_order"),


]
