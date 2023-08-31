from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from mixins.user_mixins import LoginRequiredMixin, OwnerAccessMixin
from .forms import RestaurantCreateForm, PhotoUploadForm
from .models import Restaurant, Photo


class RestaurantCreateView(LoginRequiredMixin, CreateView):
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
    template_name = 'restaurantsApp/user_restaurants.html'  # Specifica il percorso al tuo template
    context_object_name = 'objects'  # Nome del contesto da utilizzare nel template

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_delete"] = 'restaurant_delete'
        context["title_page"] = 'I miei ristoranti'
        context["obj_name"] = 'Ristoranti'

        context["obj_update"] = 'restaurant_update'
        return context

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


class RestaurantDeleteView(OwnerAccessMixin, DeleteView):
    model = Restaurant
    success_url = reverse_lazy('user_restaurants')


class RestaurantUpdateView(OwnerAccessMixin, UpdateView):
    # model = Restaurant
    form_class = RestaurantCreateForm
    success_url = reverse_lazy('user_restaurants')
    # fields = ['name', 'address', 'phone_number', 'cuisine_type','meal_type']
    template_name = 'restaurantsApp/restaurant_create.html'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Restaurant.objects.filter(restaurantID=pk)

    def get_initial(self):
        from .forms import CUISINE_CHOICES, MEAL_CHOICES

        initial = super().get_initial()
        update_obj: Restaurant = self.get_object()

        initial['cuisine_type'] = [c[0] for c in CUISINE_CHOICES if c[0] in update_obj.cuisine_type]
        initial['meal_type'] = [m[0] for m in MEAL_CHOICES if m[0] in update_obj.meal_type]

        return initial


class PhotoCreateView(OwnerAccessMixin, CreateView):
    model = Photo
    form_class = PhotoUploadForm
    success_url = reverse_lazy('user_restaurants')
    template_name = 'restaurantsApp/restaurant-add-photo.html'

    def get_initial(self):
        initial = super().get_initial()
        restaurant_id = self.kwargs.get('pk')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        initial['restaurant'] = restaurant
        return initial
