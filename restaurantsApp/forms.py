from django import forms
from django.contrib.auth.models import User

from restaurantsApp.models import Restaurant


class RestaurantCreateForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['owner', 'name', 'address', 'phone_number', 'cuisine_type', 'services', 'meal_type']


    owner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
