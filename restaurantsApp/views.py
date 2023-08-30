from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView, DetailView

from mixins.user_mixins import LoginRequiredMixin
from .forms import RestaurantCreateForm
from .models import Restaurant


class RestaurantCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = RestaurantCreateForm
    template_name = "restaurantsApp/restaurant_create.html"

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def get_success_url(self):
        # TODO mi sarebbe piaciuto aprire la detailview appena creata
        success_url = reverse_lazy("home")
        return success_url


class RestaurantOwnerListView(LoginRequiredMixin, ListView):
    model = Restaurant
    template_name = 'restaurantsApp/restaurant_list.html'  # Specifica il percorso al tuo template
    context_object_name = 'restaurants'  # Nome del contesto da utilizzare nel template

    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.filter(owner=user)


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurantsApp/restaurant_list.html'  # Specifica il percorso al tuo template
    context_object_name = 'restaurants'  # Nome del contesto da utilizzare nel template


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurantsApp/restaurant_detail.html'  # Specifica il percorso al tuo template
    context_object_name = 'restaurant'  # Nome del contesto da utilizzare nel template

