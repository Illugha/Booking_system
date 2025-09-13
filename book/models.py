from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Room(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    location = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room #{self.number} (Capacity: {self.capacity})"
    
    def is_new(self):
        return timezone.now() - self.created_at < timedelta(days=3)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"   
        ordering = ['number']


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creation_time = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100, default='Guest')
    customer_email = models.EmailField(max_length=254)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.customer_name} for Room #{self.room.number} from {self.start_time} to {self.end_time}"

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['start_time']

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f"Image for Room #{self.room.number}"

    class Meta:
        verbose_name = "Room Image"
        verbose_name_plural = "Room Images"