from django import forms
from django.contrib.auth.models import User

from restaurantsApp.RestaurantChoices import CUISINE_CHOICES, MEAL_CHOICES
from restaurantsApp.models import Restaurant, Photo


class RestaurantCreateForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['owner', 'name', 'address', 'phone_number', 'max_booking', 'cuisine_type', 'meal_type']

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
        fields = ['restaurant', 'image', 'photo_comment']

    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), widget=forms.HiddenInput())
