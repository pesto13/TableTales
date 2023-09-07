from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from restaurantsApp.models import Restaurant
from reservationsApp.models import Reservation
from datetime import datetime


class TestReservationViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            restaurantID=1,
            owner=self.user,
            name="Test Restaurant",
            address="Test Address",
            phone_number="+123456789",
            cuisine_type="italian",
            meal_type="breakfast",
            max_booking=50
        )
        # Adjust the reverse URL name based on your urls.py configuration

    def test_user_reservations_view(self):
        self.client.login(username='testuser', password='testpassword')

        Reservation.objects.create(username=self.user, restaurant=self.restaurant, how_many=5,
                                   reservation_date=datetime.now())

        url = reverse('user_reservations')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.context)
        self.assertEqual(len(response.context['objects']), 1)

    def test_reservation_delete_view(self):
        self.client.login(username='testuser', password='testpassword')

        reservation = Reservation.objects.create(username=self.user, restaurant=self.restaurant, how_many=5,
                                                 reservation_date=datetime.now())

        reservation_delete_url = reverse('reservation_delete', kwargs={'pk': reservation.pk})

        response = self.client.post(reservation_delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Reservation.objects.filter(pk=reservation.pk).exists())

