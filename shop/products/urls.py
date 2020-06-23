from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductFilteredListView.as_view(), name='products_list'),
    path('<str:slug>/', views.products_detail, name='product_detail'),
]
