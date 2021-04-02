from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    # Login system
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),


    # using name to reference for dynamic routing
    path('', views.home, name="home"),
    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account'),

    path('products/', views.products, name="products"),
    path('customer/<str:pk>', views.customer, name="customer"),

    # getting id of the customer
    path('create_order/<str:pk>', views.createOrder, name="create_order"),
    path('update_order/<str:pk>', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>', views.deleteOrder, name="delete_order"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    # uidb64: The user's id encoded in base 64
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),
    # token: Token to check that the password is valid

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),



    # 1 - Submit Email Form                       //PasswordResetView.as_view()
    # 2 - Email sent success message              //PasswordResetDoneView.as_view()
    # 3 - Link to password Reset form in email    //PasswordResetConfirmView.as_view()
    # 4 - Password successfully changed message   //PasswordResetCompleteView.as_view()
]
