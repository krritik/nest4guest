from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(GuestHouse)
admin.site.register(Rooms)
admin.site.register(Reservation)
admin.site.register(PreReservation)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(GuestDetails)
admin.site.register(Feedback)
admin.site.register(WaitingOn)