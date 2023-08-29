from datetime import datetime, time

from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

import reservationsApp.models
from mixins.user_mixins import LoginRequiredMixin
from restaurantsApp.models import Restaurant
from .forms import ReservationForm
from .models import Reservation


class ReservationCreateView(LoginRequiredMixin, CreateView):
    form_class = ReservationForm
    # fields = ['restaurant', 'username', 'reservation_date', 'entry_date', 'status']
    template_name = 'reservation_form.html'  # Modifica con il percorso corretto al tuo template

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

        #devo controllare se ho spazio
        initial['status'] = 'confirmed'

        return initial

    def form_valid(self, form):

        restaurant = form.cleaned_data.get('restaurant')
        how_many = form.cleaned_data.get('how_many')

        date = form.cleaned_data.get('reservation_date')
        date = date.date()
        start_time = make_aware(datetime.combine(date, time.min))
        end_time = make_aware(datetime.combine(date, time.max))

        #fixme le date andrebbero messe non sul giorno totale :D
        total_guests = Reservation.objects.filter(
            restaurant=restaurant,
            reservation_date__gte=start_time,
            reservation_date__lt=end_time,
            status='confirmed'
        ).aggregate(Sum('how_many'))["how_many__sum"]

        if total_guests is None:
            total_guests = 0

        if restaurant.max_booking - total_guests >= how_many:
            form.instance.status = 'confirmed'
        else:
            form.instance.status = 'pending'

        return super().form_valid(form)


class UserReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'user_reservations.html'  # Crea questo template
    context_object_name = 'reservations'

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(username=user)


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    # se uso il tastino per cancellare li sul momento non mi serve un ulteriore template
    # template_name = 'confirm_delete.html'
    success_url = reverse_lazy('user_reservations')


