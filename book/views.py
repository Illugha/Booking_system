from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

from book.models import Booking, Room

def index(request):
    bookings = Booking.objects.all()
    rooms = Room.objects.all()
    context = {
        'bookings': bookings,
        'rooms': rooms
    }
    return render(request, template_name='booking/index.html', context=context)

def all_bookings(request):
    bookings = Booking.objects.all()
    context = {'bookings': bookings}
    return render(request, 'booking/all_bookings.html', context)

def book_room(request, room_num):
    room = get_object_or_404(Room, number=room_num)

    booked = False
    error = None

    if request.method == 'POST':
        start_str = request.POST.get('start_time')
        end_str = request.POST.get('end_time')
        customer_name = request.POST.get('customer_name', 'Guest')
        customer_email = request.POST.get('customer_email')

        if start_str and end_str:
            start_time = datetime.fromisoformat(start_str)
            end_time = datetime.fromisoformat(end_str)


            overlap = Booking.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if overlap:
                error = "This room is already booked for the selected period."
            else:
                Booking.objects.create(
                    room=room,
                    start_time=start_time,
                    end_time=end_time,
                    customer_name=customer_name
                )
                booked = True


                email_title = "Booking Confirmation"
                email_body = (
                    f"Dear {customer_name},\n\n"
                    f"Your booking for Room #{room.number} from {start_time} to {end_time} has been confirmed.\n\n"
                    "Thank you!"
                )

                send_mail(
                    email_title,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [customer_email],
                    fail_silently=False,
                )

    return render(
        request,
        'booking/book_room.html',
        {'room': room, 'booked': booked, 'error': error}
    )

def info_room(request, room_num):
    room = Room.objects.get(number=room_num)
    bookings = Booking.objects.filter(room=room).order_by('start_time')
    context = {
        'room': room,
        'bookings': bookings
    }
    return render(request, 'booking/info_room.html', context)