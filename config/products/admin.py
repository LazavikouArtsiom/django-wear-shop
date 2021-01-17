from django.contrib import admin
from .models import (Size, Color, Category,
                    Sale, Product, Promocode)

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Sale)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Promocode)
admin.site.register(Product, ProductAdmin)
