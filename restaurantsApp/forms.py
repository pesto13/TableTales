from django import forms
from django.contrib.auth.models import User

from restaurantsApp.models import Restaurant, Photo


class RestaurantCreateForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['owner', 'name', 'address', 'phone_number', 'cuisine_type', 'services', 'meal_type']

    owner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())


class PhotoUploadForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['restaurant', 'image', 'photo_comment']

    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), widget=forms.HiddenInput())
