from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['restaurant', 'user', 'comment_title', 'comment', 'rating', 'cleanliness_rating', 'value_price_rating', 'service_rating', 'ambiance_rating']
        # widgets = {
        #     'rating': forms.NumberInput(attrs={'class': 'Stars'}),
        # }
