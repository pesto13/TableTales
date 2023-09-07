from django.apps import AppConfig


class ReservationsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservationsApp'

    def ready(self):
        import reservationsApp.signals
