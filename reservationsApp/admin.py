from django.contrib import admin

from reservationsApp.models import Reservation


# Register your models here.

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass