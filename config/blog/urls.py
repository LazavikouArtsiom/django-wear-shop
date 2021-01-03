from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list_url'),
    path('<slug:category_slug>/', views.post_list_by_category, name='post_list_by_category_url'),
    path('<slug:category_slug>/<slug:slug>/', views.post_detail, name='post_detail_url'),
]
