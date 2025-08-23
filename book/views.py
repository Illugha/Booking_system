from django.shortcuts import render
from book.models import Booking, Room
from datetime import datetime

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
    room = Room.objects.get(number=room_num)

    booked = Booking.objects.filter(
        room=room,
        end_time__gte=datetime.now()
    ).exists()

    if request.method == 'POST':
        start_str = request.POST.get('start_time')
        end_str = request.POST.get('end_time')
        customer_name = request.POST.get('customer_name', 'Guest')

        if start_str and end_str:
            start_time = datetime.fromisoformat(start_str)
            end_time = datetime.fromisoformat(end_str)

            Booking.objects.create(
                room=room,
                start_time=start_time,
                end_time=end_time,
                customer_name=customer_name
            )
            booked = True

    return render(request, 'booking/book_room.html', {'room': room, 'booked': booked})

def info_room(request, room_num):
    room = Room.objects.get(number=room_num)
    bookings = Booking.objects.filter(room=room).order_by('start_time')
    context = {
        'room': room,
        'bookings': bookings
    }
    return render(request, 'booking/info_room.html', context)