from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from mixins.user_mixins import LoginRequiredMixin, OwnerAccessMixin
from .forms import RestaurantCreateForm, PhotoUploadForm
from .models import Restaurant, Photo


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantCreateForm
    template_name = "form-submit.html"

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Aggiungi il tuo ristorante'
        return context

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

    def get_context_data(self, **kwargs):
        from .forms import CUISINE_CHOICES, MEAL_CHOICES
        context = super().get_context_data(**kwargs)
        context['CUISINE_CHOICES'] = CUISINE_CHOICES
        context['MEAL_CHOICES'] = MEAL_CHOICES
        return context

    def get_queryset(self):
        # Ottieni i parametri GET
        order_field = self.request.GET.get('order_field')
        filter_name = self.request.GET.get('filter_name', None)
        filter_max_booking = self.request.GET.get('filter_max_booking', None)
        cuisine_type = self.request.GET.get('filter_cuisine_type', None)
        meal_type = self.request.GET.get('filter_meal_type', None)

        queryset = Restaurant.objects.all()

        # Applica i filtri
        if filter_name:
            queryset = queryset.filter(name__icontains=filter_name)
        if filter_max_booking:
            queryset = queryset.filter(max_booking__lte=filter_max_booking)
        if cuisine_type:
            # essendo lista di stringhe uso__icontains ez
            queryset = queryset.filter(cuisine_type__icontains=cuisine_type)
        if meal_type:
            # essendo lista di stringhe uso__icontains ez
            queryset = queryset.filter(meal_type__icontains=meal_type)

        # Ordinamento
        if order_field in [field.name for field in Restaurant._meta.fields]:
            queryset = queryset.order_by(order_field)

        return queryset


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
    template_name = 'form-submit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = "Modifica il tuo ristorante"

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Restaurant.objects.filter(restaurantID=pk)

    #FIXME sembrerebbe che io l'abbia rotto :D
    def get_initial(self):
        from .forms import CUISINE_CHOICES, MEAL_CHOICES

        initial = super().get_initial()
        update_obj: Restaurant = self.get_object()

        initial['cuisine_type'] = [c[0] for c in CUISINE_CHOICES if c[0] in update_obj.cuisine_type]
        initial['meal_type'] = [m[0] for m in MEAL_CHOICES if m[0] in update_obj.meal_type]

        return initial

#TODO manca il css
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
