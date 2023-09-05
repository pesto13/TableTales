from django.urls import path

from .views import ReviewCreateView, ReviewListView, UserReviewsListView, ReviewDeleteView

urlpatterns = [

    # path('', ReviewListView.as_view(), name='review_list'),
    path('create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),

    path('reviews/', UserReviewsListView.as_view(), name='user_reviews'),
]
