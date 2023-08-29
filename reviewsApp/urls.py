from django.urls import path

from .views import ReviewCreateView, ReviewListView, UserReviewsListView

urlpatterns = [

    path('', ReviewListView.as_view(), name='review_list'),
    path('create/', ReviewCreateView.as_view(), name='review_create'),

    #TODO sistema
    path('reviews/', UserReviewsListView.as_view(), name= 'user_reviews'),
]