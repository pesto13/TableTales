from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Reservation
from django.db.models import Sum


@receiver(post_delete, sender=Reservation)
def post_delete_handler(sender, instance, **kwargs):
    restaurant = instance.restaurant
    date = instance.reservation_date

    total_guests = Reservation.objects.filter(
        restaurant=restaurant,
        reservation_date=date,
        status='confirmed'
    ).aggregate(Sum('how_many'))["how_many__sum"] or 0 # nel caso in cui ci siano 0 entry sarebbe null altrimenti

    available_seats = restaurant.max_booking - total_guests

    pending_reservation = Reservation.objects.filter(
        restaurant=restaurant,
        reservation_date=date,
        status='pending',
        how_many__lte=available_seats

    ).first()

    if pending_reservation:
        print(f"{pending_reservation}, sta per essere introdotta")
        pending_reservation.status = 'confirmed'
        pending_reservation.save()
    else:
        print("nulla da fare")



