from django.test import TestCase
from django.contrib.auth.models import User
from restaurantsApp.models import Restaurant, Photo
from reviewsApp.models import Review


class RestaurantModelTests(TestCase):

    def setUp(self):
        # Create a test user for restaurant owner.
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a restaurant for testing.
        self.restaurant = Restaurant.objects.create(
            restaurantID=1,
            owner=self.user,
            name="Test Restaurant",
            address="123 Test Street",
            phone_number="+1234567890",
            cuisine_type="[italian, japanese]",
            meal_type="[lunch, dinner]",
            max_booking=50
        )

    def test_restaurant_creation(self):
        """Test if the restaurant is created and saved correctly."""
        self.assertEqual(self.restaurant.name, "Test Restaurant")
        self.assertEqual(self.restaurant.address, "123 Test Street")

    def test_average_rating_update(self):
        """Test the average_rating_update method."""
        Review.objects.create(
            restaurant=self.restaurant,
            username=self.user,
            comment_title="Good experience!",
            comment="The food was tasty and service was quick.",
            rating=3
        )
        Review.objects.create(
            restaurant=self.restaurant,
            username=self.user,
            comment_title="Good experience!",
            comment="The food was tasty and service was quick.",
            rating=5
        )

        self.assertEqual(self.restaurant.average_rating_update(), 4)

    def test_meal_type_as_list(self):
        """Test the meal_type_as_list method."""
        self.assertEqual(self.restaurant.meal_type_as_list(), ['Pranzo', 'Cena'])

    def test_cuisine_type_as_list(self):
        """Test the cuisine_type_as_list method."""
        self.assertEqual(self.restaurant.cuisine_type_as_list(), ['Italiana', 'Giapponese'])

    # You can add more tests for other methods as well.


class PhotoModelTests(TestCase):

    def setUp(self):
        # Assuming a setup similar to RestaurantModelTests
        self.user = User.objects.create_user(username='testuser', password='testpassword')
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
        self.photo = Photo.objects.create(
            photoID=1,
            restaurant=self.restaurant,
            photo_comment="Test Comment"
        )

    def test_photo_creation(self):
        """Test if the photo is created and saved correctly."""
        self.assertEqual(self.photo.photo_comment, "Test Comment")
        self.assertEqual(self.photo.restaurant.name, "Test Restaurant")
