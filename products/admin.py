from django.contrib import admin
from .models import Product, Category, Genre, Artist, Publisher

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Publisher)