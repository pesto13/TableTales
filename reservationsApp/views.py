from django.db.models import Sum
from django.views.generic.edit import CreateView

from mixins.user_mixins import LoginRequiredMixin
from restaurantsApp.models import Restaurant
from .forms import ReservationForm
from .models import Reservation


class ReservationCreateView(LoginRequiredMixin, CreateView):
    form_class = ReservationForm
    # fields = ['restaurant', 'username', 'reservation_date', 'entry_date', 'status']
    template_name = 'reservation_form.html'  # Modifica con il percorso corretto al tuo template
    success_url = '/'  # Modifica con l'URL di reindirizzamento desiderato

    def get_initial(self):
        initial = super().get_initial()

        # Imposta il valore iniziale del campo "restaurant" con l'oggetto ristorante
        restaurant_id = self.kwargs.get('pk')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        initial['restaurant'] = restaurant

        initial['username'] = self.request.user

        #devo controllare se ho spazio
        initial['status'] = 'confirmed'

        return initial

    def form_valid(self, form):
        # Esegui il controllo delle prenotazioni qui
        restaurant = form.cleaned_data.get('restaurant')
        how_many = form.cleaned_data.get('how_many')
        total_guests = Reservation.objects.filter(
            restaurant=restaurant,
            status='confirmed'
        ).aggregate(Sum('how_many'))["how_many__sum"]

        if restaurant.max_booking - total_guests < how_many:
            form.instance.status = 'pending'
        else:
            form.instance.status = 'confirmed'

        return super().form_valid(form)
