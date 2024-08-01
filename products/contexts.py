from .models import Genre, Product
from django.db.models import Count

def top_genres(request):
    top_genres = Genre.objects.annotate(num_products=Count('product')).exclude(name__iexact='sale').order_by('-num_products')[:10]
    return {'top_genres': top_genres}