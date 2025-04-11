from django.contrib import admin
from . import models

admin.site.register(models.Train)
admin.site.register(models.User)
admin.site.register(models.Station)
admin.site.register(models.Schedule)
admin.site.register(models.Coach)
admin.site.register(models.Seat)
admin.site.register(models.Passenger)
admin.site.register(models.Booking)
admin.site.register(models.Ticket)
admin.site.register(models.Payment)
admin.site.register(models.Route)
admin.site.register(models.Availability)
