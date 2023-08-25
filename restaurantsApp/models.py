from django.db import models

# Create your models here.

from django.db import models

from django.conf import settings


# TODO questa è una prima versione veloce, sistemare i tipi
class Restaurant(models.Model):
    RestaurantID = models.IntegerField(primary_key=True)
    Owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Address = models.CharField(max_length=200)
    PhoneNumber = models.CharField(max_length=20)
    CuisineType = models.CharField(max_length=50)
    Services = models.CharField(max_length=200)
    MealType = models.CharField(max_length=100)
    # PhotoURL = models.URLField()

    def __str__(self):
        return self.Name
