from django.contrib import admin
from .models import Product, Category, Genre, Artist, Publisher

# Inline class to manage Genres within Product
class GenreInline(admin.TabularInline):  # You can also use StackedInline
    model = Product.genres.through
    extra = 1

# Admin class for Product
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
    inlines = [GenreInline]
    exclude = ('genres',)

# Admin class for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

# Admin class for Artist
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'website',
    )    
    ordering = ('name',)

# Admin class for Publisher
class PublisherAdmin(admin.ModelAdmin):
    ordering = ('name',)

# Admin class for Genre
class GenreAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Publisher, PublisherAdmin)
