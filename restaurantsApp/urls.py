from django.urls import path

from .views import RestaurantCreateView, RestaurantListView, RestaurantDetailView

urlpatterns = [

    path("", RestaurantListView.as_view(), name="listRestaurants"),

    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path("add/", RestaurantCreateView.as_view(), name="addRestaurant"),

]