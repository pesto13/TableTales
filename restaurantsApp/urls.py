from django.urls import path

from .views import *

urlpatterns = [

    path("", RestaurantListView.as_view(), name="listRestaurants"),

    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),

    #per owner
    path("create/", RestaurantCreateView.as_view(), name='restaurant_create'),
    path("<int:pk>/delete/", RestaurantDeleteView.as_view(), name='restaurant_delete'),
    path("own-restaurants/", RestaurantOwnerListView.as_view(), name='user_restaurants'),


]