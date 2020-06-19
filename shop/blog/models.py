from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill



class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique = True, default='', db_index=True)
    image = models.ImageField(upload_to='blog/category/detail', null=True, blank=True)
    image_header = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(1920, 239)],
            options={'quality': 90})
    

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f'/blog/{self.slug}/'


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='title')
    slug = models.SlugField(unique = True, default='', db_index=True)
    text = models.TextField(verbose_name='text', default='TEXT')

    image = models.ImageField(upload_to='blog/post/detail/', null=True, blank=True)
    image_for_index = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(720, 539)],
            options={'quality': 90})
    image_for_list_and_detail = ImageSpecField(source='image', format='JPEG', processors=[ResizeToFill(820, 481)],
            options={'quality': 90})

    category = models.ForeignKey(Category, 
                                related_name='category',
                                null=True,
                                blank=True,
                                verbose_name='category',
                                on_delete=models.CASCADE)
    published_date = models.DateField(default=timezone.now ,blank=True, null=True)

    class Meta:
        ordering = ('published_date',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
            return self.title

    def get_absolute_url(self):
        return f'/blog/{self.category.slug}/{self.slug}/'


