from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), #using name to reference for dynamic routing
    path('products/', views.products, name="products"),
    path('customer/<str:pk>', views.customer, name="customer"),
]