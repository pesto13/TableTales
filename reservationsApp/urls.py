from django.urls import path
from .views import ReservationCreateView, UserReservationsView

urlpatterns = [
    # Altre URL...
    path('create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/', UserReservationsView.as_view(), name='user_reservations'),
]
