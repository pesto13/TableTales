from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from reviewsApp.models import Review
from restaurantsApp.models import Restaurant

class ReviewModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
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
            comment_title='Amazing!',
            comment='The food was delicious.',
            rating=5
        )

    def test_review_creation(self):
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(self.review.comment_title, 'Amazing!')

    def test_str_representation(self):
        self.assertEqual(str(self.review), f"Review for {self.restaurant} by {self.user.username}")

    def test_str_for_logged_user(self):
        formatted_str = self.review.str_for_logged_user()
        self.assertIn(str(self.review.review_date.date()), formatted_str)
        self.assertIn("Valutazione: 5", formatted_str)
        self.assertIn("Commento: The food was delicious.", formatted_str)

    def test_rating_validators(self):
        # Test rating less than 1
        with self.assertRaises(ValidationError):
            review = Review.objects.create(
                restaurant=self.restaurant,
                username=self.user,
                comment_title='Too Low!',
                comment='This rating should fail.',
                rating=0
            )
            review.full_clean()

        # Test rating more than 5
        with self.assertRaises(ValidationError):
            review = Review.objects.create(
                restaurant=self.restaurant,
                username=self.user,
                comment_title='Too High!',
                comment='This rating should fail.',
                rating=6
            )
            review.full_clean()
