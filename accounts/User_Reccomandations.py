
from restaurantsApp.models import Restaurant
from reservationsApp.models import Reservation
from reviewsApp.models import Review


class UserRecommendations:
    def __init__(self, user):
        self.user = user

        self.reviews = Review.objects.all().filter(username=user)
        self.reservations = Reservation.objects.all().filter(username=user)

        # questo viene calcolato sulla base di questi sopra
        self.coefficients: dict[str, float]

    def calculate_coefficients(self):
        cuisine_counter = dict()
        for r in self.reviews:
            for ct in r.restaurant.cuisine_type_as_list():
                if ct in cuisine_counter:
                    cuisine_counter[ct] += 1
                else:
                    cuisine_counter[ct] = 1

        print(cuisine_counter)

