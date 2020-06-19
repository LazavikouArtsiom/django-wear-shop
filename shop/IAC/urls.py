from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index_url'),
    path('contact/', views.contact, name='contact_url'),
    path('about/', TemplateView.as_view(template_name='IAC/about.html')),
]
