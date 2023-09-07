from django.urls import path

from .views import ReviewCreateView, UserReviewsListView, ReviewDeleteView

urlpatterns = [


    path('create/', ReviewCreateView.as_view(), name='review_create'),

    path('reviews/', UserReviewsListView.as_view(), name='user_reviews'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),

]
