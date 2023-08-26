from django.conf import settings
from django.db import models

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

    def __str__(self):
        return f"Reservation for {self.restaurant.name} by {self.username.name}"
