from django.shortcuts import render, redirect
from products.models import Product, Category
from blog.models import Post
from .forms import ContactForm
from .models import Contact
from cart.utils import get_cart_items, get_total_price
from django.views.generic import TemplateView

def index(request):
    featured_products_ids = [product.id for product in Product.objects.all() if product.is_new()]
    featured_products = Product.objects.filter(id__in=featured_products_ids)
    categories = Category.objects.all()[0:6]
    posts = Post.objects.all().order_by('published_date')
    items = get_cart_items(request)

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'posts': posts,
        'items': items,
        'total_price': get_total_price(items)
    }

    return render(request, template_name='IAC/index.html', context=context)


def contact(request):
    template_name = 'IAC/contact.html'

    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            content = request.POST.get('text')
            mail = request.POST.get('mail')
            username = request.POST.get('username')
            contact = Contact.objects.create(username=username, mail=mail ,text=content)
            contact.save()
            return redirect('/contact/')
    else: 
        contact_form = ContactForm()
    items = get_cart_items(request)
    

    context = {
        'contact_form':contact_form,
        'items': items,
        'total_price': get_total_price(items)
    }
    return render(request, template_name, context)


class about(TemplateView):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        items = get_cart_items(request)
        context['items'] = items
        context['total_price'] = get_total_price(items)
        return self.render_to_response(context)


    