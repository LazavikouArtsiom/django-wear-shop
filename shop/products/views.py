from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage
from .models import Product, Category, Color
from .filters import ProductFilter
from django import forms
from django.shortcuts import get_object_or_404
# from .forms import ProductChangeForm

def products_list(request):

    template_name = 'products/product-list.html'
    products_list = Product.objects.all().order_by('price')
    categories = Category.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products_list)
    products_list = product_filter.qs
    quantity = products_list.count()

    if products_list:
        min_price = products_list.first().price
        max_price = products_list.last().price

    paginator = Paginator(products_list, 16)
    page = request.GET.get('page')
    try:
        products = paginator.page(page) 
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = { 'products': products,
                'categories': categories,
                'product_filter': product_filter,
                'quantity': quantity,
                }

    if products_list:
        context['max_price'] = max_price
        context['min_price'] = min_price

    return render(request, template_name, context)

def products_list_by_category(request, category_slug):
    template_name = 'products/product-list.html'
    products_list = Product.objects.filter(category__slug=category_slug).order_by('price')
    searched_category = get_object_or_404(Category, slug__iexact=category_slug)
    categories = Category.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products_list)
    products_list = product_filter.qs
    quantity = products_list.count()

    if products_list:
        min_price = products_list.first().price
        max_price = products_list.last().price
    paginator = Paginator(products_list, 16)
    page = request.GET.get('page')

    try:
        products = paginator.page(page) 
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = { 'products': products,
                'categories': categories,
                'product_filter': product_filter,
                'quantity': quantity,
                'searched_category':searched_category,
                }

    if products_list:
        context['max_price'] = max_price
        context['min_price'] = min_price
    return render(request, template_name, context)

def products_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug__iexact=slug, category__slug=category_slug)
    sizes = product.size.all()
    colors = product.color.all()
    related_products = Product.objects.filter(color__in=colors).exclude(name=product.name)

    class ProductDetailForm(forms.Form):
        SIZE_CHOICES = [(choice.name, choice) for choice in sizes]
        COLOR_CHOICES = [(choice.name, choice) for choice in colors]

        size_choice_field = forms.ChoiceField(choices=SIZE_CHOICES, widget=forms.Select(attrs={'class': 'class="select2-selection select2-selection--single"'}))
        color_choice_field = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.Select(attrs={'class': 'class="select2-selection select2-selection--single"'}))   
        quantity = forms.IntegerField(initial=1)

    form = ProductDetailForm()
    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'form': form,
        'related_products': related_products,
    }

    return render(request, 'products/product-detail.html', context)

# def products_detail_change(request, category_slug, slug):
#     product = get_object_or_404(Product, slug__iexact=slug, category__slug=category_slug)
#     form = ProductChangeForm()

#     if request.method == 'POST':
#         form = ProductChangeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             product.name = form.cleaned_data['name']
#             product.slug = form.cleaned_data['slug']
#             product.price = form.cleaned_data['price']
#             product.image = form.cleaned_data['image']
#             product.size = form.cleaned_data['size']
#             product.color = form.cleaned_data['color']
#             product.sale = form.cleaned_data['sale']

#             return redirect(product)
#     else:
#         form = ProductChangeForm()

#     context = {
#         'product': product,
#         'form': form,
#     }
#     return render(request, template_name='products/product-detail-change.html', context=context)