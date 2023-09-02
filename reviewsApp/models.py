from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings
from django.template.defaultfilters import linebreaksbr


# from restaurantsApp.models import Restaurant

# Create your models here.


class Review(models.Model):
    restaurant = models.ForeignKey('restaurantsApp.Restaurant', on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_title = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.restaurant} by {self.username}"

    def str_for_logged_user(self):
        return linebreaksbr(
            f"Recensione per {self.restaurant} in data {self.review_date.date()}"
            f"\n Valutazione: {self.rating}"
            f"\n Commento: {self.comment}"
        )
