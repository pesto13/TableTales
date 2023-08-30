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

    def get_initial(self):
        initial = super().get_initial()
        restaurant_id = self.kwargs.get('pk')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        initial['restaurant'] = restaurant
        initial['username'] = self.request.user

        return initial

    def get_success_url(self):
        # Ottieni la chiave primaria (pk) del ristorante dalla richiesta
        restaurant_pk = self.kwargs.get('pk')
        success_url = reverse_lazy('restaurant_detail', kwargs={'pk': restaurant_pk})
        return success_url


class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'  # Modifica con il percorso corretto al tuo template
    context_object_name = 'reviews'  # Nome della variabile di contesto nel template


class UserReviewsListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'user-object-list.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_delete"] = 'review_delete'
        context["title_page"] = 'Le mie recensioni'
        context["obj_name"] = 'Recensioni'
        return context

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(username=user)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('user_reviews')

