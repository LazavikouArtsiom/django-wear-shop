import django_filters
from .models import Product
from django import forms
from .models import Color, Size, Category


class ProductFilter(django_filters.FilterSet):

    SIZE_CHOICES = [(choice.name, choice) for choice in Size.objects.all()]

    COLOR_CHOICES = [(choice.name, choice) for choice in Color.objects.all()]

    CATEGORY_CHOICES = [(choice.name, choice) for choice in Category.objects.all()]
    

    ORDER_CHOICES = (
        ('ascending', 'ascending'),
        ('descending', 'descending'),
    )

    PRICE_CHOICES = (
        ('from_0_to_50', '$0.00 - $50.00'),
        ('from_50_to_100', '$50.00 - $100.00'),
        ('from_100_to_150', '$100.00 - $150.00'),
        ('from_150_to_200', '$150.00 - $200.00'),
        ('from_200', '$200.00+'),
    )

    SALE_CHOICES = (
        ('1', 'with sale'),
    )

    category = django_filters.ChoiceFilter(label='category', choices=CATEGORY_CHOICES, method='filter_by_category')
    ordering = django_filters.ChoiceFilter(label='ordering', choices=ORDER_CHOICES, method='filter_by_order')
    price = django_filters.ChoiceFilter(label='price', choices=PRICE_CHOICES, method='filter_by_price')
    color = django_filters.ChoiceFilter(label='color', choices=COLOR_CHOICES, method='filter_by_color')
    size = django_filters.ChoiceFilter(label='size', choices=SIZE_CHOICES, method='filter_by_size')
    sale = django_filters.ChoiceFilter(label='sale', choices=SALE_CHOICES, method='filter_by_sale')

    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
        }
        
    
    def filter_by_order(self, queryset, name, value):
        expression = 'price' if value == 'ascending' else '-price'
        return queryset.order_by(expression)

    def filter_by_price(self, queryset, name, value):
        if value == 'from_0_to_50':
            return queryset.filter(price__gte=0, price__lte=50)
        elif value == 'from_50_to_100':
            return queryset.filter(price__gte=50, price__lte=100)
        elif value == 'from_100_to_150':
            return queryset.filter(price__gte=100, price__lte=150)
        elif value == 'from_150_to_200':
            return queryset.filter(price__gte=150, price__lte=200)
        elif value == 'from_200':
            return queryset.filter(price__gte=200)
    
    def filter_by_color(self, queryset, name, value):
        return queryset.filter(color__name__iexact=value)

    def filter_by_size(self, queryset, name, value):
        return queryset.filter(size__name__iexact=value)
    
    def filter_by_category(self, queryset, name, value):
        return queryset.filter(category__name__exact=value)

    def filter_by_sale(self, queryset, name, value):
        return queryset.filter(sale__isnull=False) 


