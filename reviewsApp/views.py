from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from django.views.generic.edit import CreateView, DeleteView

from mixins.user_mixins import LoginRequiredMixin
from restaurantsApp.models import Restaurant
from .forms import ReviewForm
from .models import Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'review_form.html'
    #TODO cambia manca la pk :D
    # success_url = /url/to/detailrestaurant/
    success_url = '/'

    def get_initial(self):
        initial = super().get_initial()

        # Imposta il valore iniziale del campo "restaurant" con l'oggetto ristorante
        restaurant_id = self.kwargs.get('pk')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        initial['restaurant'] = restaurant

        initial['username'] = self.request.user

        return initial


class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'  # Modifica con il percorso corretto al tuo template
    context_object_name = 'reviews'  # Nome della variabile di contesto nel template


class UserReviewsListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'user_reviews.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(username=user)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    # template non serve
    success_url = reverse_lazy('user_reviews')

