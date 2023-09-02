from django.conf import settings
from django.db import models
from django.template.defaultfilters import linebreaksbr

from restaurantsApp.models import Restaurant

# Create your models here.


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField()
    entry_date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('confirmed', 'Confermata'),
        ('pending', 'In attesa'),
        ('cancelled', 'Cancellata'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    how_many = models.IntegerField()

    def __str__(self):
        return f"Reservation for {self.restaurant.name} by {self.username} with {self.how_many} people"

    def str_for_logged_user(self):
        return linebreaksbr(
            f"Prenotazione per {self.restaurant} "
            f"in data {self.reservation_date.date()} alle {self.reservation_date.time()}"
            f"\n Numero di persone: {self.how_many}"
            f"\n Stato: {self.status}"
        )
