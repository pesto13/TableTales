

from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils import timezone

from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

from mixins.user_mixins import LoginRequiredMixin
from restaurantsApp.models import Restaurant
from .forms import ReservationForm
from .models import Reservation


class ReservationCreateView(LoginRequiredMixin, CreateView):
    form_class = ReservationForm
    template_name = 'form-submit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = "Inserisci la tua prenotazione"
        return context

    def get_success_url(self):
        # Ottieni la chiave primaria (pk) del ristorante dalla richiesta
        restaurant_pk = self.kwargs.get('pk')
        success_url = reverse_lazy('restaurant_detail', kwargs={'pk': restaurant_pk})
        return success_url

    def get_initial(self):
        initial = super().get_initial()

        # Imposta il valore iniziale del campo "restaurant" con l'oggetto ristorante
        restaurant_id = self.kwargs.get('pk')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        initial['restaurant'] = restaurant

        initial['username'] = self.request.user

        initial['status'] = 'confirmed'

        return initial

    def form_valid(self, form):

        restaurant = form.cleaned_data.get('restaurant')
        how_many = form.cleaned_data.get('how_many')

        reservation_date = form.cleaned_data.get('reservation_date')

        # # Calcola l'ora 1 prima della prenotazione
        # one_hour_before = reservation_date - timedelta(hours=1)
        #
        # # Calcola l'ora 2 dopo la prenotazione
        # two_hours_after = reservation_date + timedelta(hours=2)

        total_guests = Reservation.objects.filter(
            restaurant=restaurant,
            reservation_date=reservation_date,
            status='confirmed'
        ).aggregate(Sum('how_many'))["how_many__sum"] or 0

        if restaurant.max_booking - total_guests >= how_many:
            form.instance.status = 'confirmed'
        else:
            form.instance.status = 'pending'

        if reservation_date <= timezone.now():
            # Aggiungi un errore al form
            form.add_error('reservation_date', 'La data di prenotazione deve essere futura.')
            return super().form_invalid(form)

        return super().form_valid(form)


class UserReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'user-object-list.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_delete"] = 'reservation_delete'
        context["title_page"] = 'Le mie prenotazioni'
        context["obj_name"] = 'Prenotazioni'
        return context

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(username=user)


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    success_url = reverse_lazy('user_reservations')
