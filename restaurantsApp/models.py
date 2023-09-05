import datetime
from datetime import timedelta, datetime

from django.db import models
from django.conf import settings
from django.db.models import Sum

from phonenumber_field.modelfields import PhoneNumberField

from restaurantsApp.RestaurantChoices import MEAL_CHOICES, CUISINE_CHOICES
from reviewsApp.models import Review


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

    def cuisine_list(self):
        return self._split_substrings(self.cuisine_type)

    @staticmethod
    def _generate_dates(chosen_date):
        # TODO potrebbe essere un attributo
        opening_hour = 10
        closing_hour = 20
        current_date = chosen_date.replace(hour=opening_hour, minute=0, second=0, microsecond=0)
        end_time = chosen_date.replace(hour=closing_hour, minute=0, second=0, microsecond=0)

        while current_date < end_time:
            yield current_date
            current_date += timedelta(hours=1)

    def available_hours_list(self):
        available_hours = dict()

        today = datetime.now()
        for actual_hour in self._generate_dates(today):
            one_hour_before = actual_hour - timedelta(hours=1)
            two_hours_after = actual_hour + timedelta(hours=2)

            total_guests = self.reservation_set.all().filter(
                reservation_date__gte=one_hour_before,
                reservation_date__lt=two_hours_after,
                status='confirmed'
            ).aggregate(Sum('how_many'))["how_many__sum"]

            available_hours[actual_hour.time()] = total_guests

        return available_hours

class Photo(models.Model):
    photoID = models.IntegerField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')
    photo_comment = models.CharField(max_length=100, default="")

    class Meta:
        ordering = ['-photoID']
