from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Artist, Publisher, Genre

class ArtistForm(forms.ModelForm):
    
    class Meta:
        model = Artist
        fields = ['name', 'description', 'website']

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Publisher Name'})
        }

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Genre Name'})
        }

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'category',
            'title',
            'artist',
            'publisher',
            'genres',
            'pages',
            'description',
            'price',
            'sku',
            'cover_type',
            'color_option',
            'image_url',
            'image',
            'rating',
            'date_added'
        ]

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'