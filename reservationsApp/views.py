from django.views.generic.edit import CreateView

from mixins.user_mixins import LoginRequiredMixin
from restaurantsApp.models import Restaurant
from .forms import ReservationForm


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

        return initial
