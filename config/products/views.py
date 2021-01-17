from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, Category, Color
from .filters import ProductFilter
from django import forms
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView
from cart.utils import get_cart_items, get_total_price
from django.db import connection


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filtered_data = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filtered_data.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filtered_data'] = self.filtered_data
        context['product_filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        items = get_cart_items(self.request)
        context['items'] = items
        context['total_price'] = get_total_price(items)

        if self.kwargs.get('category_slug', None):
            context['searched_category'] = get_object_or_404(Category, slug__iexact=self.request.GET['category'])
        return context


class ProductFilteredListView(FilteredListView):
    queryset = Product.objects.all().order_by('-price')
    template_name = 'products/product-list.html'
    paginate_by = 12
    context_object_name = 'products'
    allow_empty = True
    filterset_class = ProductFilter




def products_detail(request, slug):
    product = get_object_or_404(Product, slug__iexact=slug)
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
    items = get_cart_items(request)
    total_price = get_total_price(items)
    context = {
        'product': product,
        'items': items,
        'total_price': total_price,
        'sizes': sizes,
        'colors': colors,
        'form': form,
        'related_products': related_products,
    }

    return render(request, 'products/product-detail.html', context)
