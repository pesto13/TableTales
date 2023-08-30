from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from restaurantsApp.models import Restaurant

class LoginRequiredMixin(UserPassesTestMixin):
    def __init__(self):
        self.request = None

    def test_func(self):
        return self.request.user.is_authenticated


class OwnerAccessMixin(UserPassesTestMixin):
    """
    Mixin che permette l'accesso solo al proprietario del ristorante.
    """

    def __init__(self):
        self.kwargs = None
        self.request = None

    def test_func(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        return restaurant.owner == self.request.user
