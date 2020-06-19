from django.db import models
from django.conf import settings
from products.models import Product, Color, Size

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = [['user', 'product', 'product', 'size', 'color']]

    def __str__(self):
        return f'{self.user} | {self.product} | {self.size} | {self.color} | {self.quantity}'

    def calculate_price(self):
        return self.product.calculate_price() * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=0
    )
    cart_items = models.ManyToManyField(CartItem, related_name='cart_items')
    
    def __str__(self):
        return f'{self.user.username} Cart'
    
    def get_cart_items(self):
        return self.cart_items.all()
    
    def get_total_price(self):
        return sum([(item.product.calculate_price() * item.quantity) for item in self.cart_items.all()])
