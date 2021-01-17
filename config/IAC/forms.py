from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea(attrs= {'class': '', 'placeholder': 'message*'}), label='')
    username = forms.CharField(widget=forms.TextInput(attrs= {'class': '', 'placeholder': 'username*'}), label='')
    mail = forms.CharField(widget=forms.TextInput(attrs= {'class': '', 'placeholder': 'mail*'}), label='')

    
    class Meta:
        model = Contact
        fields = ['username','mail']
