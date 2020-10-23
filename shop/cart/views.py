from django.shortcuts import render, get_object_or_404, redirect, reverse
from products.models import Product
from .models import CartItem, Cart, Size, Color
from time import sleep
from .decorators import user_authenticated
from django.db import IntegrityError

@user_authenticated
def add_to_cart(request, slug):
    sleep(1)
    product = get_object_or_404(Product, slug__iexact=slug)
    user = request.user

    if not Cart.objects.filter(user=user).first():
        cart = Cart.objects.create(user=user)
    else:
        cart = Cart.objects.get(user=user)
       
    if request.POST:
        color_req = request.POST.get('color_choice_field')
        size_req = request.POST.get('size_choice_field')
        color = Color.objects.get(name=color_req)
        size = Size.objects.get(name=size_req)
        quantity = request.POST.get('quantity', 1)
    else:
        color = product.color.first()
        size = product.size.first()
        quantity = 1

    try:
        item = CartItem.objects.create(product=product, color=color, size=size, user=user, quantity=quantity)
        cart.cart_items.add(item)
    except IntegrityError:
        pass

    category = product.category.name.replace(' ', '+') 

    return redirect(request.META['HTTP_REFERER'])


@user_authenticated
def cart_list(request):
    user = request.user
    items = user.cart.cart_items.all()
    cart = user.cart
    template_name = 'cart/cart.html'

    context = {
        'items': items,
        'cart': cart,
    }

    return render(request, template_name, context)