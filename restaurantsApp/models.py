from django.db import models
from django.conf import settings
from django.template.defaultfilters import linebreaksbr
from phonenumber_field.modelfields import PhoneNumberField
from reviewsApp.models import Review

CUISINE_CHOICES = (
        ('italian', 'Italiana'),
        ('japanese', 'Giapponese'),
        ('indian', 'Indiana'),
        ('mexican', 'Messicana'),
        ('chinese', 'Cinese'),
        ('seafood', 'Pesce'),
        ('steakhouse', 'Steakhouse'),
        ('barbecue', 'Barbecue'),
        ('tigelle', 'Tigelle'),
        ('pizza', 'Pizza'),
    )

MEAL_CHOICES = (
        ('breakfast', 'Colazione'),
        ('lunch', 'Pranzo'),
        ('happy_hour', 'Aperitivo'),
        ('dinner', 'Cena'),
    )


# TODO questa è una prima versione veloce, sistemare i tipi
class Restaurant(models.Model):
    restaurantID = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    cuisine_type = models.CharField(max_length=200)
    meal_type = models.CharField(max_length=200)
    max_booking = models.IntegerField(default=100)
    average_rating = models.FloatField(default=0, null=True)

    def __str__(self):
        return self.name

    def str_for_logged_user(self):
        return self.name

    def average_rating_update(self):
        reviews = self.review_set.all()  # Ottieni tutte le recensioni associate al ristorante
        if reviews:
            media = sum(review.rating for review in reviews) / len(reviews)
            return round(media, 2)  # Arrotonda la media a due decimali
        return 0  # Nessuna recensione

    @staticmethod
    def _split_substrings(input_string):
        cleaned_string = input_string.strip('[]').replace(' ', '').replace("'", '')
        substrings = cleaned_string.split(',')
        return substrings

    def meal_type_as_list(self):
        return [m[1] for m in MEAL_CHOICES if m[0] in self._split_substrings(self.meal_type)]

    def cuisine_type_as_list(self):
        return [c[1] for c in CUISINE_CHOICES if c[0] in self._split_substrings(self.cuisine_type)]


class Photo(models.Model):
    photoID = models.IntegerField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')
    photo_comment = models.CharField(max_length=100, default="")
