from django import forms
from django.contrib.auth.models import User

from restaurantsApp.models import Restaurant
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['restaurant', 'user', 'comment_title', 'comment', 'rating', 'cleanliness_rating', 'value_price_rating', 'service_rating', 'ambiance_rating']
        # widgets = {
        #     'rating': forms.NumberInput(attrs={'class': 'Stars'}),
        # }

    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), widget=forms.HiddenInput())
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())