from django.db import models
from django.utils import timezone

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Publisher(models.Model):
    name = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=254, unique=True)
    description = models.TextField(blank=True, default="This is a great artist.")
    website = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    COLOR_CHOICES = [
        ('colour', 'Colour'),
        ('black_and_white', 'Black and White'),
        ('colour_bw', 'Colour + B&W'),
    ]

    artist = models.ForeignKey('Artist', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    publisher = models.ForeignKey('Publisher', null=True, blank=True, on_delete=models.SET_NULL)
    genres = models.ManyToManyField('Genre', blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    title = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    cover_type = models.CharField(max_length=50, choices=[('softcover', 'Softcover'), ('hardcover', 'Hardcover')])
    color_option = models.CharField(max_length=20, choices=COLOR_CHOICES, default='colour')
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
