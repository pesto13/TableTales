class UserRecommendations:
    def __init__(self, user, reviews):
        self.user = user

        self.reviews = reviews
        # self.reservations = Reservation.objects.all().filter(username=user)
        # questo viene calcolato sulla base di questi sopra
        self.coefficients = dict()
        self.actual_cuisine_coefficients = dict()
        self.actual_meal_coefficients = dict()

    # OK
    def calculate_review_coefficients(self):
        cuisine_counter = dict()
        # per ogni review che ho fatto
        for rev in self.reviews:
            # guardo il ristorante e vedo che Cuisine Type
            for ct in rev.restaurant.cuisine_list():
                # ci sommo il rating
                if ct in cuisine_counter:
                    cuisine_counter[ct] += rev.rating
                else:
                    cuisine_counter[ct] = rev.rating

        cuisine_sum = sum([value for value in cuisine_counter.values()])

        # do un valore percentuale per il rating
        for key, value in cuisine_counter.items():
            self.coefficients[key] = value/cuisine_sum*100

    # OK
    def _calculate_actual_restaurant_coefficients(self, actual_restaurant):
        # conteggio
        cuisine_type_counter = {ct: 1 for ct in actual_restaurant.cuisine_list()}
        meal_type_counter = {mt: 1 for mt in actual_restaurant.cuisine_list()}

        # calcolo del peso di ogni voce
        for key in cuisine_type_counter.keys():
            self.actual_cuisine_coefficients[key] = 100/len(cuisine_type_counter.keys())

        # calcolo del peso di ogni voce

        for key in meal_type_counter.keys():
            self.actual_meal_coefficients[key] = 100/len(meal_type_counter.keys())

        # print(self.actual_meal_coefficients, self.actual_cuisine_coefficients)

    def get_recommended_restaurants(self, all_restaurants, actual_restaurant):
        restaurant_review_points = dict()
        actual_restaurant_points = dict()

        # punteggi delle review
        for restaurant in all_restaurants:
            restaurant_review_points[restaurant] = self._get_review_score(restaurant)

        self._calculate_actual_restaurant_coefficients(actual_restaurant)

        # punteggi del actual_restaurant
        for restaurant in all_restaurants:
            actual_restaurant_points[restaurant] = self._get_actual_cuisine_score(restaurant)

        # qua devo fare i trucchi

        definitive_points = self._mix_points(
            (
                restaurant_review_points,
                actual_restaurant_points
             ),
            (
                0.3,
                0.7
            )
        )

        sorted_restaurant_points = dict(sorted(definitive_points.items(), key=lambda x: x[1], reverse=True))
        print(sorted_restaurant_points)
        return list(sorted_restaurant_points.keys())

    # sembra ok
    def _get_review_score(self, restaurant):
        return sum([self.coefficients.get(cuisine_type, 0) for cuisine_type in restaurant.cuisine_list()])

    def _get_actual_cuisine_score(self, restaurant):
        return sum([self.actual_cuisine_coefficients.get(cuisine_type, 0) for cuisine_type in restaurant.cuisine_list()])

    @staticmethod
    def _mix_points(dicts, weights):
        mixed_points = {}
        keys = dicts[0].keys()
        for key in keys:
            combined_value = sum(dizionario[key] * peso for dizionario, peso in zip(dicts, weights))
            mixed_points[key] = combined_value

        return mixed_points
