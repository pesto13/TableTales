from django import forms
from django.contrib.auth.models import User

from restaurantsApp.models import Restaurant
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['restaurant', 'username', 'comment_title', 'comment', 'rating']

    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), widget=forms.HiddenInput())
    username = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
