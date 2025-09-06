from django.contrib import admin
from book.models import Booking, Room, RoomImage

admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(RoomImage)