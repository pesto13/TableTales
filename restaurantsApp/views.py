from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from accounts.User_Reccomandations import UserRecommendations
from mixins.user_mixins import LoginRequiredMixin, OwnerAccessMixin
from reviewsApp.models import Review
from .forms import RestaurantCreateForm, PhotoUploadForm
from .models import Restaurant


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
    paginate_by = 6

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
        filter_average_rating = self.request.GET.get('filter_average_rating', None)
        cuisine_type = self.request.GET.get('filter_cuisine_type', None)
        meal_type = self.request.GET.get('filter_meal_type', None)

        queryset = Restaurant.objects.all()

        # Applica i filtri
        if filter_name:
            queryset = queryset.filter(name__icontains=filter_name)
        if filter_max_booking:
            queryset = queryset.filter(max_booking__lte=filter_max_booking)
        if filter_average_rating:
            queryset = queryset.filter(average_rating__lte=int(filter_average_rating)+1)
            queryset = queryset.filter(average_rating__gt=int(filter_average_rating))
        if cuisine_type:
            # essendo lista di stringhe uso__icontains ez
            queryset = queryset.filter(cuisine_type__icontains=cuisine_type)
        if meal_type:
            # essendo lista di stringhe uso__icontains ez
            queryset = queryset.filter(meal_type__icontains=meal_type)

        # Ordinamento

        if order_field == "average_rating":
            return queryset.order_by("average_rating").reverse()

        if order_field in [field.name for field in Restaurant._meta.fields]:
            queryset = queryset.order_by(order_field)

        return queryset


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurantsApp/restaurant-detail-v2.html'  # Specifica il percorso al tuo template
    context_object_name = 'restaurant'  # Nome del contesto da utilizzare nel template

    # def _get_recommended_restaurants(self):
    #     user = self.request.user
    #     user_reviews = Review.objects.all().filter(username=user)
    #     user_reservations = Reservation.objects.all().filter(username=user)
    #
    #     return rest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user = self.request.user
            ur = UserRecommendations(self.request.user, Review.objects.all().filter(username=user))
            ur.calculate_review_coefficients()

            context['recommend_restaurant_list'] = ur.get_recommended_restaurants(
                # tutti i ristoranti tranne quello attuale
                Restaurant.objects.all().exclude(restaurantID=self.object.restaurantID),
                # il ristorante attuale
                self.object
            )
        return context


class RestaurantDeleteView(OwnerAccessMixin, DeleteView):
    model = Restaurant
    success_url = reverse_lazy('user_restaurants')


class RestaurantUpdateView(OwnerAccessMixin, UpdateView):
    form_class = RestaurantCreateForm
    success_url = reverse_lazy('user_restaurants')

    template_name = 'form-submit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = "Modifica il tuo ristorante"
        return context

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
    # model = Photo
    form_class = PhotoUploadForm
    success_url = reverse_lazy('user_restaurants')
    template_name = 'form-submit.html'

    def get_initial(self):
        initial = super().get_initial()
        restaurant_id = self.kwargs.get('pk')
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            initial['restaurant'] = restaurant
        except Restaurant.DoesNotExist:
            raise Http404("Il ristorante specificato non esiste.")
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = "Aggiungi una foto"
        return context

# class RestaurantCreateView(LoginRequiredMixin, CreateView):
#     model = Restaurant
#     form_class = RestaurantCreateForm
#     template_name = 'restaurantsApp/restaurant-form.html'
#     success_url = reverse_lazy('home')
#
#     def get_initial(self):
#         initial = super().get_initial()
#         initial['owner'] = self.request.user
#         return initial
#
#     def form_valid(self, form):
#
#         restaurant_form = RestaurantCreateForm(self.request.POST)
#         photo_form = PhotoUploadForm(self.request.POST, self.request.FILES)
#
#         if all([photo_form.is_valid(), restaurant_form.is_valid()]):  # Check if the photo form is valid
#             r = restaurant_form.save(commit=True)
#
#             photo = photo_form.save(commit=False)  # Save the photo form data but don't commit to the database yet
#             photo.restaurant = r  # Assuming there is a ForeignKey field in your Photo model to associate it with a restaurant
#             photo.save()  # Commit the photo data to the database
#
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # Aggiungi il formset inline per le foto al contesto
#
#         context['photo_form'] = PhotoUploadForm
#
#         return context
