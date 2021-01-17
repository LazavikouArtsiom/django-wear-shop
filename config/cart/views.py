from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from products.models import Product
from .models import CartItem, Size, Color, Order
from time import sleep
from django.db import IntegrityError
from django.contrib.auth.models import AnonymousUser
from .utils import *
from .forms import OrderCreationForm


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug__iexact=slug)

    try:
        add_item_to_session(request, product)
    except AlreadyInCartExeption:
        pass
    
    return redirect(request.META['HTTP_REFERER'])
    

def cart_list(request):
    items = get_cart_items(request)
    total_price = get_total_price(items)
    template_name = 'cart/cart.html'

    context = {
        'items': items,
        'total_price': total_price,
        'form': OrderCreationForm,
    }

    if request.POST:
        
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            human = True

        try:
            order = create_order(request)
        except CartIsEmptyException:
            return HttpResponse(status=403)

        if request.session.get('orders', False):
            request.session['orders'] += f'{str(order.id)};'
        else:
            request.session['orders'] = f'{str(order.id)};'
    else:
        form = OrderCreationForm()

    return render(request, template_name, context)


def orders_list(request):
    items = get_cart_items(request)
    total_price = get_total_price(items)
    orders = get_orders_list_from_session(request)
    template_name = 'cart/orders.html'
    
    context = {
        'items': items,
        'total_price': total_price,
        'orders':orders,
    }

    return render(request, template_name, context)