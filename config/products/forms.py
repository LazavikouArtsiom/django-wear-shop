# from django import forms
# from .models import Product, Size, Color, Sale

# class ProductChangeForm(forms.ModelForm):

#     sizes = Size.objects.all()
#     colors = Color.objects.all()
#     sales = Sale.objects.all()

#     SIZE_CHOICES = [(choice.name, choice) for choice in sizes]
#     COLOR_CHOICES = [(choice.name, choice) for choice in colors]
#     SALE_CHOICES = [(choice.percent, choice) for choice in sales]

#     size_choice_field = forms.ChoiceField(choices=SIZE_CHOICES, widget=forms.Select(attrs={'class': 'class="select2-selection select2-selection--single"'}))
#     color_choice_field = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.Select(attrs={'class': 'class="select2-selection select2-selection--single"'}))   
#     sale_choice_field = forms.ChoiceField(choices=SALE_CHOICES, widget=forms.Select(attrs={'class': 'class="select2-selection select2-selection--single"'}))   

#     class Meta:
#         model = Product
#         fields = ['name','slug','price',
#                   'image']


