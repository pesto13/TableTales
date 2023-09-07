from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from restaurantsApp.models import Restaurant, Review

User = get_user_model()


class ReviewViewsTest(TestCase):

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

        self.review = Review.objects.create(
            restaurant=self.restaurant,
            username=self.user,
            rating=4,
            comment="Good food!"
        )

        self.client = Client()

    def test_review_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('review_create', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lascia una recensione')

        post_data = {
            "rating": 5,
            "comment": "Excellent!",
            "restaurant": self.restaurant.pk,
            "username": self.user.pk
        }

        response = self.client.post(reverse('review_create', args=[self.restaurant.pk]), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Excellent!')


    def test_user_reviews_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Good food!')


