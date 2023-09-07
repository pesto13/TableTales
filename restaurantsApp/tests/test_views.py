from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from restaurantsApp.models import Restaurant, Review
# Se stai usando Factory Boy o un altro pacchetto simile, importa le tue factories qui

User = get_user_model()

class RestaurantViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.restaurant = Restaurant.objects.create(
            restaurantID=1,
            owner=self.user,
            name="Test Restaurant",
            address="Test Address",
            phone_number="+123456789",
            cuisine_type="italian",
            meal_type="breakfast"
        )

        self.client = Client()

    def test_restaurant_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('restaurant_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aggiungi il tuo ristorante')

        post_data = {
            "name": "New Test Restaurant",
            "address": "New Test Address",
            "phone_number": "+987654321",
            "cuisine_type": "italian",
            "meal_type": "dinner"
        }

        response = self.client.post(reverse('restaurant_create'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Test Restaurant')

    def test_restaurant_owner_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user_restaurants'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'I miei ristoranti')
        self.assertContains(response, 'Test Restaurant')

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('listRestaurants'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')

    def test_restaurant_detail_view(self):
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')

    def test_restaurant_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('restaurant_delete', args=[self.restaurant.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Restaurant')

    def test_restaurant_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('restaurant_update', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Modifica il tuo ristorante')

    def test_photo_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('photo_create', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aggiungi una foto')

