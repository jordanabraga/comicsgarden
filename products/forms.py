from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Artist, Publisher, Genre

class ArtistForm(forms.ModelForm):    
    class Meta:
        model = Artist
        fields = ['name', 'description', 'website']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Artist.objects.filter(name=name).exists():
            raise forms.ValidationError("An artist with this name already exists.")
        return name

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Publisher.objects.filter(name=name).exists():
            raise forms.ValidationError("A publisher with this name already exists.")
        return name

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Genre.objects.filter(name=name).exists():
            raise forms.ValidationError("A genre with this name already exists.")
        return name

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

        # Retrieve categories and set choices
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names

        # Retrieve genres, sort alphabetically, and set queryset
        genres = Genre.objects.all().order_by('name')
        self.fields['genres'].queryset = genres

        # Apply CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'