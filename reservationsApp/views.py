from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView

from .forms import ReservationForm
from .models import Reservation


class ReservationCreateView(CreateView):
    form_class = ReservationForm
    # fields = ['restaurant', 'username', 'reservation_date', 'entry_date', 'status']
    template_name = 'reservation_form.html'  # Modifica con il percorso corretto al tuo template
    success_url = '/'  # Modifica con l'URL di reindirizzamento desiderato

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)