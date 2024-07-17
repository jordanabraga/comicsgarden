from django.contrib import admin
from .models import Product, Category, Genre, Artist, Publisher

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'artist',
        'publisher',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'website',
    )    

    ordering = ('name',)

class PublisherAdmin(admin.ModelAdmin):
    ordering = ('name',)

class GenreAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Publisher, PublisherAdmin)