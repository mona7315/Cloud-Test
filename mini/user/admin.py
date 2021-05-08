from webbrowser import register
from django.contrib.auth.models import Permission

from django.contrib import admin

from user.models import Room, Booking
# Register your models here.
admin.site.register(Room)

admin.site.register(Booking)

admin.site.register(Permission)
