from django.urls import path

from .views import ReviewCreateView, ReviewListView

urlpatterns = [

    path('', ReviewListView.as_view(), name='review_list'),
    path('create/', ReviewCreateView.as_view(), name='review_create'),

]