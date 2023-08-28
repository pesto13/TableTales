from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['restaurant', 'username', 'reservation_date', 'status']
        widgets = {
            'reservation_date': DateTimePickerInput(options={
                "format": "DD/MM/YYYY hh:mm",
                "showTodayButton": True,
                # FIXME
                # "autoclose": True,
                # "step": "30",
            }),
        }




