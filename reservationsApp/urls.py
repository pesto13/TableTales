from django.urls import path
from .views import ReservationCreateView

urlpatterns = [
    # Altre URL...
    path('create/', ReservationCreateView.as_view(), name='reservation_create'),
]
