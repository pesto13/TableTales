from django.db import models

# Create your models here.

from django.db import models

from django.conf import settings


# TODO questa è una prima versione veloce, sistemare i tipi
class Restaurant(models.Model):
    restaurantID = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=20)
    cuisineType = models.CharField(max_length=50)
    services = models.CharField(max_length=200)
    mealType = models.CharField(max_length=100)
    # PhotoURL = models.URLField()

    def __str__(self):
        return self.name
