from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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

            if not overlap:
                email_title = "Booking Confirmation"
                html_content = render_to_string("booking/booking_email.html", {
                    'room': room,
                    'start_time': start_time,
                    'end_time': end_time,
                    'customer_name': customer_name
                    })
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    email_title,
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [customer_email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                Booking.objects.create(
                    room=room,
                    start_time=start_time,
                    end_time=end_time,
                    customer_name=customer_name,
                    customer_email=customer_email
                ).save()
                booked = True
            
    return render(
        request,
        'booking/book_room.html',
        {'room': room, 'booked': booked, 'error': error}
    )

def confirm_booking(request, room_id):
    booking = get_object_or_404(Booking, room_id=room_id, confirmed=False)
    if not booking.confirmed:
        booking.confirmed = True
        booking.save()
        message = "Your booking has been confirmed. Thank you!"
    else:
        message = "This booking has already been confirmed."
    
    return render(request, 'booking/confirm_booking.html', {'message': message, 'booking': booking})

def info_room(request, room_num):
    room = Room.objects.get(number=room_num)
    bookings = Booking.objects.filter(room=room).order_by('start_time')
    context = {
        'room': room,
        'bookings': bookings
    }
    return render(request, 'booking/info_room.html', context)