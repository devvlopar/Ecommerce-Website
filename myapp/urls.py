from . import views
from django.urls import path
from django.views import View

urlpatterns = [    
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('products/',views.products,name='products'),
    path('cart/',views.cart,name='cart'),
    path('delete_cart/<int:pk>',views.delete_cart,name='delete_cart'),
    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('payment/', views.homepage, name='home')


]