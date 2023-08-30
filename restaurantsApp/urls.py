from django.urls import path

from .views import *

urlpatterns = [

    path("", RestaurantListView.as_view(), name="listRestaurants"),

    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),

    #per owner
    path("create/", RestaurantCreateView.as_view(), name='restaurant_create'),
    path("<int:pk>/delete/", RestaurantDeleteView.as_view(), name='restaurant_delete'),
    path("<int:pk>/update/", RestaurantUpdateView.as_view(), name='restaurant_update'),
    path("own-restaurants/", RestaurantOwnerListView.as_view(), name='user_restaurants'),
    path("<int:pk>/photo/", PhotoCreateView.as_view(), name='photo_create'),


]