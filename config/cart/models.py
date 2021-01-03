from django.db import models
from django.conf import settings
from products.models import Product, Color, Size
from phonenumber_field.modelfields import PhoneNumberField

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = [['product', 'size', 'color', 'quantity']]

    def __str__(self):
        return f'{self.product} | {self.size} | {self.color} | {self.quantity}'

    def calculate_price(self):
        return self.product.calculate_price() * self.quantity


class Order(models.Model):
    DELIVERY_CHOICES = (
        ('pick_up', 'Pick up'),
        ('courier', 'Courier')
    )

    ORDER_STATUS_CHOICES = (
        ('created', 'Created'),
        ('payment', 'Payment'),
        ('availabilty', 'Availability'),
        ('shipping', 'Shipping'),
        ('delivery_date', 'Delivery date'),
    )

    PAYMENT_CHOICES = (
        ('receipt', (
                    ('CR', 'Cash'),
                    ('BCR', 'Bank card'),
                    ('GCR', 'Gift card'),
                    )),
        ('pay_now', (
                    ('ICN','installment card'),
                    ('BKN','Visa, Mastercard, Belcard'),
                    ('EN','ERIP')
                    )),
        ('partial', 'Partial payment'),
        ('legal_persons', 'Legal persons'),
    )

    items = models.ManyToManyField(CartItem)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=70, default='')
    delivery = models.CharField(max_length=30, choices=DELIVERY_CHOICES, default='pick_up')
    phone_number = PhoneNumberField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    payment = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='CR', blank=True)
    promocode = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='created')
    total_price = models.IntegerField(default=0)
    user_ip = models.CharField(max_length=15, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    #LEGAL 
    BIC = models.CharField(max_length=9, blank=True, null=True)
    UNP = models.CharField(max_length=9, blank=True, null=True)
    IBAN = models.CharField(max_length=28, blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    legal_address = models.CharField(max_length=200, blank=True, null=True)
    legal_name = models.CharField(max_length=200, blank=True, null=True)
    supply_agreement = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}|{self.status}'

    class Meta:
        unique_together = [['user_ip', 'date_created']]