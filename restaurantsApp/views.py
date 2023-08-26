from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView, DetailView

from .models import Restaurant


class RestaurantCreateView(generic.CreateView):
    model = Restaurant
    # fields = ['Owner', 'Name', 'Address', 'PhoneNumber', 'CuisineType', 'Services', 'MealType', 'PhotoURL']
    fields = ['Owner', 'Name', 'Address', 'PhoneNumber', 'CuisineType', 'Services', 'MealType']
    #TODO mi sarebbe piaciuto aprire la detailview appena creata
    success_url = reverse_lazy("listRestaurants")
    template_name = "restaurantsApp/addRestaurant.html"


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurantsApp/restaurant_list.html'  # Specifica il percorso al tuo template
    context_object_name = 'restaurants'  # Nome del contesto da utilizzare nel template


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurantsApp/restaurant_detail.html'  # Specifica il percorso al tuo template
    context_object_name = 'restaurant'  # Nome del contesto da utilizzare nel template
