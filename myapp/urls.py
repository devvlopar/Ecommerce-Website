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
]