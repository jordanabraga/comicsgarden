from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Artist, Publisher, Genre

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    artists = None
    publishers = None
    genres = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        
        if 'artist' in request.GET:
            artists = request.GET['artist'].split(',')
            products = products.filter(artist__name__iexact=artists)
            artists = Artist.objects.filter(name__in=artists)

        if 'publisher' in request.GET:
            publishers = request.GET['publisher'].split(',')
            products = products.filter(publisher__name__iexact=publishers)
            publishers = Publisher.objects.filter(name__in=publishers)

        if 'genre' in request.GET:
            genres = request.GET['genre'].split(',')
            products = products.filter(genres__name__iexact=query)
            genres = Genre.objects.filter(name__in=genres)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(title__icontains=query) | Q(artist__name__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_artists': artists,
        'current_publishers': publishers,
        'current_genres': genres,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)