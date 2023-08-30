from django.contrib import admin
from .models import Restaurant, Photo


# Register your models here.

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
