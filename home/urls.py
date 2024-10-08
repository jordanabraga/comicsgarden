from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about_view, name='about'),
    path('shipping/', views.shipping_view, name='shipping'),
]