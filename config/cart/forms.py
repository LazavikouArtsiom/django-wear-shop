from django import forms
from .models import Order
from captcha.fields import CaptchaField

class OrderCreationForm(forms.ModelForm):
    captcha = CaptchaField()
    
    class Meta:
        model = Order
        exclude = ('items','status','total_price',)
        