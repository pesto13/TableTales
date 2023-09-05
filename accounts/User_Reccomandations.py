import math

from restaurantsApp.models import Restaurant
from reservationsApp.models import Reservation
from reviewsApp.models import Review
from restaurantsApp.RestaurantChoices import *


class UserRecommendations:
    def __init__(self, user, reviews):
        self.user = user

        self.reviews = reviews
        # self.reservations = Reservation.objects.all().filter(username=user)
        # questo viene calcolato sulla base di questi sopra
        self.coefficients = dict()

    def calculate_coefficients(self):
        cuisine_counter = dict()

        # questo li conta tutto con successo :D
        for rev in self.reviews:
            for ct in rev.restaurant.cuisine_list():
                if ct in cuisine_counter:
                    cuisine_counter[ct] += rev.rating
                else:
                    cuisine_counter[ct] = rev.rating

        cuisine_sum = sum([value for value in cuisine_counter.values()])

        for key, value in cuisine_counter.items():
            self.coefficients[key] = value/cuisine_sum*100

    def get_recommended_restaurants(self, all_restaurants):
        restaurant_points = dict()
        for restaurant in all_restaurants:
            restaurant_points[restaurant] = self._get_score(restaurant)

        sorted_restaurant_points = dict(sorted(restaurant_points.items(), key=lambda x: x[1], reverse=True))
        return list(sorted_restaurant_points.keys())

    def _get_score(self, restaurant):
        return sum([self.coefficients.get(cuisine_type, 0) for cuisine_type in restaurant.cuisine_list()])
