from django.contrib import admin

from reviewsApp.models import Review


# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
