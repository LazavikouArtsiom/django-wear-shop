from products.models import Product
from .models import CartItem, Order, Size, Color
from products.models import Promocode
from django.contrib.auth.models import AnonymousUser

class AlreadyInCartExeption(Exception):
    def __init__(self, message="Item is already in the cart"):
        self.message = message
        super().__init__(self.message)

class CartIsEmptyException(Exception):
    def __init__(self, message="Cart is empty"):
        self.message = message
        super().__init__(self.message)

def add_item_to_session(request, product):
    if request.POST:
        color = Color.objects.get(name=request.POST.get("color_choice_field"))
        size = Size.objects.get(name=request.POST.get("size_choice_field"))
        new_quantity = request.POST.get("quantity", 1)
        if request.session.get('cart_items', False):
            if request.session['cart_items'].find(f'{product.slug},{color},{size}') != -1:
                raise AlreadyInCartExeption
            request.session['cart_items'] += f'{product.slug},{color},{size},{new_quantity};'
        else:
            request.session['cart_items'] = f'{product.slug},{color},{size},{new_quantity};'
        return True
    else:
        if not request.session.get('cart_items', False):
            request.session['cart_items'] = f'{product.slug},{product.color.first()},{product.size.first()},1;'                                        
        else:
            if request.session['cart_items'].find(f'{product.slug},{product.color.first()},{product.size.first()}') != -1:
                raise AlreadyInCartExeption
            request.session['cart_items'] += f'{product.slug},{product.color.first()},{product.size.first()},1;'                                        
        return True

def get_cart_items(request):
    try:
        cart_items = request.session.get('cart_items', False).split(';')
    except AttributeError:
        return []
    cart_items = list(filter(None, cart_items))
    qs = []
    for item in cart_items:
        try:
            slug, color, size, quantity = item.split(',')
        except ValueError:
            pass


        try:
            product = Product.objects.get(slug=slug)
        except ValueError:
            continue


        try:
            color = Color.objects.get(name=color)
            size = Size.objects.get(name=size)
        except NameError:
            size = Product.size.first()
            color = Product.color.first()

        item = CartItem.objects.get_or_create(product=product, color=color, size=size, quantity=quantity)[0]
        qs.append(item)
    return qs

def get_total_price(items):
    price = 0
    for item in items:
        price += int(item.calculate_price())
    return price

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def calculate_price_with_promocode(promocode, price):
    return price - price * (Promocode.objects.get(code=promocode).percent * 0.01)

def create_order(request):
    items = get_cart_items(request)
    if not items:
        raise CartIsEmptyException
    price = get_total_price(items)

    promocode = request.POST['promocode']
    if promocode:
        price = calculate_price_with_promocode(promocode, price)
    address = request.POST['address']
    email = request.POST['email']
    delivery = request.POST['delivery']
    phone_number = request.POST['phone_number']
    comment = request.POST['comment']
    payment = request.POST['payment']
    BIC = request.POST['BIC']
    UNP = request.POST['UNP']
    IBAN = request.POST['IBAN']
    bank = request.POST['bank']
    legal_address = request.POST['legal_address']
    legal_name = request.POST['legal_name']

    if request.POST['supply_agreement'] == 'on':
        supply_agreement = True
    else:
        supply_agreement = False

    order = Order.objects.create(address=address, email=email, delivery=delivery, 
                            phone_number=phone_number, comment=comment, payment=payment, 
                            promocode=promocode, BIC=BIC, UNP=UNP, IBAN=IBAN, bank=bank,
                            legal_address=legal_address, legal_name=legal_name, supply_agreement=supply_agreement,
                            total_price=price, user_ip=get_client_ip(request))
        
    for item in items:
        order.items.add(item)
    order.save()

    request.session['cart_items'] = ''
    return order


def get_orders_list_from_session(request):
    result = []
    try:
        orders = list(map(int, list(filter(None, request.session['orders'].split(';')))))
    except ValueError:
        return result
    
    for order_id in orders:
        order = Order.objects.filter(id=order_id)
        if order:
            result += order
    return result