from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.

from django.views.generic.edit import CreateView
from .models import Review


class ReviewCreateView(CreateView):
    model = Review
    fields = ['restaurant', 'user', 'comment_title', 'comment', 'rating', 'cleanliness_rating', 'value_price_rating', 'service_rating', 'ambiance_rating']
    template_name = 'review_form.html'  # Modifica con il percorso corretto al tuo template
    success_url = '/'  # Modifica con l'URL di reindirizzamento desiderato


    #TODO passare i valori già correti, questo non funziona
    def form_valid(self, form):
        form.instance.user = self.request.user  # Imposta l'utente corrente come autore della recensione
        # form.instance.restaurant = 3
        return super().form_valid(form)


class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'  # Modifica con il percorso corretto al tuo template
    context_object_name = 'reviews'  # Nome della variabile di contesto nel template
