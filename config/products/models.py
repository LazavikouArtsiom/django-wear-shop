from django.db import models
from django.utils.timezone import timedelta
from datetime import timedelta, timezone
from datetime import datetime
from django.shortcuts import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Promocode(models.Model):
    code = models.CharField(max_length=30)
    percent = models.IntegerField(default=0)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'promocode'


class Size(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='size'
        verbose_name_plural='sizes'


class Color(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='color'
        verbose_name_plural='colors'


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True)
    image = models.ImageField(upload_to='products/category/detail', null=True, blank=True)

    image_header = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(1920, 239)],
            options={'quality': 90})
    # index page
    image_list = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(720, 660)],
            options={'quality': 90})
    image_list_2 = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(720, 932)],
            options={'quality': 90})
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        name = self.__str__().replace(' ', '+')
        return f'/products/?category={ name }'
        # return reverse('products_list_by_category', kwargs={'category_slug': self.slug,})


class Sale(models.Model):
    percent = models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.percent)
    
    class Meta:
        verbose_name='sale'
        verbose_name_plural='sales'


class Product(models.Model):

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, db_index=True, unique=True)
    price = models.IntegerField(verbose_name='price')
    category = models.ForeignKey(Category, related_name='category', verbose_name='category',
                                 on_delete=models.CASCADE, default='0')

    size = models.ManyToManyField(Size, related_name='size', verbose_name='size')

    color = models.ManyToManyField(Color, related_name='color', verbose_name='color',
                                blank=True)

    sale = models.ForeignKey(Sale, related_name='sale',
                                null=True, blank=True, verbose_name='sale',
                                on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created')

    image = models.ImageField(upload_to='products/product/detail', null=True, blank=True)

    image_2 = models.ImageField(upload_to='products/product/detail', null=True, blank=True)

    image_3 = models.ImageField(upload_to='products/product/detail', null=True, blank=True)

    image_list = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(720, 960)],
            options={'quality': 90})
    image_cart = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(320, 320)],
            options={'quality': 90})
    # index page
    image_detail_lg = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(1200, 1600)],
            options={'quality': 90})
    image_detail_lg_2 = ImageSpecField(source='image_2', format='JPEG', processors=[ResizeToFill(1200, 1600)],
            options={'quality': 90})
    image_detail_lg_3 = ImageSpecField(source='image_3', format='JPEG', processors=[ResizeToFill(1200, 1600)],
            options={'quality': 90})
    image_detail = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(320, 427)],
            options={'quality': 90})
    image_detail_2 = ImageSpecField(source='image_2', format='JPEG', processors=[ResizeToFill(320, 427)],
            options={'quality': 90})
    image_detail_3 = ImageSpecField(source='image_3', format='JPEG', processors=[ResizeToFill(320, 427)],
            options={'quality': 90})


    class Meta:
        ordering = ('name', 'created_at',)
        index_together = ('id', 'slug')
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    def has_sale(self):
        return self.sale

    def calculate_price(self):
        if self.sale:
            return self.price - (self.price * self.sale.percent * 0.01)
        else:
            return self.price

    def is_new(self):
        new_days = 14
        now = datetime.now(tz=timezone.utc)
        return now - self.created_at < timedelta(days=new_days)


    

