from django.urls import path
from book import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<int:room_num>', views.book_room, name='book_room'),
    path('info_room/<int:room_num>', views.info_room, name='info_room'),
    path('all_bookings/', views.all_bookings, name='all_bookings'),
]