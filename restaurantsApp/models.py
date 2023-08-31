from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from reviewsApp.models import Review


# TODO questa è una prima versione veloce, sistemare i tipi
class Restaurant(models.Model):
    restaurantID = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    cuisine_type = models.CharField(max_length=200)
    # services = models.CharField(max_length=200)
    meal_type = models.CharField(max_length=200)
    max_booking = models.IntegerField(default=100)

    average_rating = models.FloatField(default=0, null=True)

    def __str__(self):
        return self.name

    def average_rating_update(self):
        reviews = self.review_set.all()  # Ottieni tutte le recensioni associate al ristorante
        if reviews:
            media = sum(review.rating for review in reviews) / len(reviews)
            return round(media, 2)  # Arrotonda la media a due decimali
        return 0  # Nessuna recensione


class Photo(models.Model):
    photoID = models.IntegerField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')
    photo_comment = models.CharField(max_length=100, default="")
