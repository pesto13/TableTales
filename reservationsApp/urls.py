from django.urls import path
from .views import ReservationCreateView, UserReservationsView, ReservationDeleteView

urlpatterns = [
    # Altre URL...
    path('create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/', UserReservationsView.as_view(), name='user_reservations'),

    path('<int:pk>/delete', ReservationDeleteView.as_view(), name='reservation_delete'),
]
