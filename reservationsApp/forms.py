from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from django.contrib.auth.models import User

from restaurantsApp.models import Restaurant
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['restaurant', 'username', 'reservation_date', 'how_many', 'status']
        widgets = {
            'reservation_date': DateTimePickerInput(options={
                "format": "DD/MM/YYYY hh:mm",
                "showTodayButton": True,
                # FIXME
                # "autoclose": True,
                # "step": "30",
            }),
        }

    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), widget=forms.HiddenInput())
    username = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())






