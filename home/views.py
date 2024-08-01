from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')

def about_view(request):
    return render(request, 'home/about.html')

def shipping_view(request):
    return render(request, 'home/shipping.html')