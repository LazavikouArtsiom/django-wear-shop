from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('<str:category_slug>/', views.products_list_by_category, name='products_list_by_category'),
    path('<str:category_slug>/<str:slug>/', views.products_detail, name='product_detail'),
    # path('<str:category_slug>/<str:slug>/change/', views.products_detail_change, name='product_detail_change_url'),
]
