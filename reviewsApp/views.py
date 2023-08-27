from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.

from django.views.generic.edit import CreateView

from restaurantsApp.models import Restaurant
from .forms import ReviewForm
from .models import Review


class ReviewCreateView(CreateView):
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = '/'


    def get_initial(self):
        #il campo va messo hidden ma usando il field corretto
        initial = super().get_initial()

        # Imposta il valore iniziale del campo "restaurant" con l'oggetto ristorante
        restaurant_id = self.kwargs.get('pk')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        initial['restaurant'] = restaurant

        return initial


class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'  # Modifica con il percorso corretto al tuo template
    context_object_name = 'reviews'  # Nome della variabile di contesto nel template
