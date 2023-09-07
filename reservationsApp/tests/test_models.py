from django.test import TestCase
from django.contrib.auth.models import User
from reservationsApp.models import Reservation
from restaurantsApp.models import Restaurant
from datetime import datetime, timedelta


class ReservationModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant = Restaurant.objects.create(
            restaurantID=1,
            owner=self.user,
            name="Test Restaurant",
            address="123 Test Street",
            phone_number="+1234567890",
            cuisine_type="[Italian, French]",
            meal_type="[Lunch, Dinner]",
            max_booking=50
        )
        self.reservation_time = datetime.now() + timedelta(days=1)
        self.reservation = Reservation.objects.create(
            restaurant=self.restaurant,
            username=self.user,
            reservation_date=self.reservation_time,
            status='pending',
            how_many=3
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.restaurant, self.restaurant)
        self.assertEqual(self.reservation.username, self.user)
        self.assertEqual(self.reservation.status, 'pending')
        self.assertEqual(self.reservation.how_many, 3)

    def test_reservation_str(self):
        expected_string = f"Reservation for {self.restaurant.name} by {self.user.username} with 3 people"
        self.assertEqual(str(self.reservation), expected_string)

    def test_reservation_status_choices(self):
        self.assertIn(('confirmed', 'Confermata'), Reservation.STATUS_CHOICES)
        self.assertIn(('pending', 'In attesa'), Reservation.STATUS_CHOICES)
        self.assertIn(('cancelled', 'Cancellata'), Reservation.STATUS_CHOICES)
