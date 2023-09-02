from django import forms
from django.contrib.auth.models import User

from restaurantsApp.models import Restaurant, Photo

CUISINE_CHOICES = (
        ('italian', 'Italiana'),
        ('japanese', 'Giapponese'),
        ('indian', 'Indiana'),
        ('mexican', 'Messicana'),
        ('chinese', 'Cinese'),
        ('seafood', 'Pesce'),
        ('steakhouse', 'Steakhouse'),
        ('barbecue', 'Barbecue'),
        ('tigelle', 'Tigelle'),
        ('pizza', 'Pizza'),
    )

MEAL_CHOICES = (
        ('breakfast', 'Colazione'),
        ('lunch', 'Pranzo'),
        ('happy_hour', 'Aperitivo'),
        ('dinner', 'Cena'),
    )


class RestaurantCreateForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['owner', 'name', 'address', 'phone_number', 'cuisine_type', 'meal_type']

    cuisine_type = forms.MultipleChoiceField(
        choices=CUISINE_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    meal_type = forms.MultipleChoiceField(
        choices=MEAL_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    owner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())


class PhotoUploadForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['image', 'photo_comment']

    # restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), widget=forms.HiddenInput())
