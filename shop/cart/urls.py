from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('add_to_cart/<str:slug>/', views.add_to_cart, name='add_to_cart_url'),
    path('cart/', views.cart_list, name='cart_url'),
]
