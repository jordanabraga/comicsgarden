from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, Artist, Genre, Publisher, Wishlist
from .forms import ProductForm, ArtistForm, PublisherForm, GenreForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    
    product = get_object_or_404(Product, pk=product_id)
    in_wishlist = False
    
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    context = {
        'product': product,
        'in_wishlist': in_wishlist,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product, artist, publisher, or genre to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    # Initialize forms
    product_form = ProductForm()
    artist_form = ArtistForm()
    publisher_form = PublisherForm()
    genre_form = GenreForm()

    if request.method == 'POST':
        # Handle Product Form Submission
        if 'add_product' in request.POST:
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product = product_form.save()
                messages.success(request, 'Successfully added product!')
                return redirect(reverse('product_detail', args=[product.id]))
            else:
                messages.error(request, 'Failed to add product. Please ensure the form is valid.')
        
        # Handle Artist Form Submission
        elif 'add_artist' in request.POST:
            artist_form = ArtistForm(request.POST, request.FILES)
            if artist_form.is_valid():
                artist_form.save()
                messages.success(request, 'Successfully added artist!')
                return redirect(reverse('add_product'))
            else:
                messages.error(request, 'Failed to add artist. An artist with this name already exists.')

        # Handle Publisher Form Submission
        elif 'add_publisher' in request.POST:
            publisher_form = PublisherForm(request.POST)
            if publisher_form.is_valid():
                publisher_form.save()
                messages.success(request, 'Successfully added publisher!')
                return redirect(reverse('add_product'))
            else:
                messages.error(request, 'Failed to add publisher. A publisher with this name already exists.')

        # Handle Genre Form Submission
        elif 'add_genre' in request.POST:
            genre_form = GenreForm(request.POST)
            if genre_form.is_valid():
                genre_form.save()
                messages.success(request, 'Successfully added genre!')
                return redirect(reverse('add_product'))
            else:
                messages.error(request, 'Failed to add genre. A genre with this name already exists.')

    template = 'products/add_product.html'
    context = {
        'product_form': product_form,
        'artist_form': artist_form,
        'publisher_form': publisher_form,
        'genre_form': genre_form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing a product.')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


#Wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f"{product.title} has been added to your wishlist.")
    else:
        messages.info(request, f"{product.title} is already in your wishlist.")
    return redirect('product_detail', product_id=product.id)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.filter(user=request.user, product=product).first()
    if wishlist:
        wishlist.delete()
        messages.success(request, f"{product.title} has been removed from your wishlist.")
    else:
        messages.info(request, f"{product.title} was not in your wishlist.")
    return redirect('product_detail', product_id=product.id)

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})