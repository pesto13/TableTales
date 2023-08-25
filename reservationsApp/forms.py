from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['restaurant', 'username', 'reservation_date', 'entry_date', 'status']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'datetime-local'}),
            'entry_date': forms.DateInput(attrs={'type': 'datetime-local'}),
        }
