from __future__ import annotations

from . import models
from datetime import datetime, timedelta, date
from django.core.paginator import Paginator


class BookingOption:

    def __init__(self, room: models.Room, date_arrival: date, days: int):
        self.room = room
        self.days = int(days)
        self.date_arrival = date_arrival
        self.date_departure = date_arrival + timedelta(days=self.days)
        self.price = self.room.category.price * self.days


class Search:

    DEFAULT_LIMIT = 10

    def __init__(self):
        pass

    def search(self, date_arrival: date|str, days: int, category: int = None, room: int = None, tenants: int = None,
               offset: int = None, limit: int = DEFAULT_LIMIT):

        if not date_arrival:
            date_arrival = datetime.now().date()

        if not days:
            days = 7

        if isinstance(date_arrival, str):
            date_arrival = datetime.strptime(date_arrival, '%d.%m.%Y')
            if not date_arrival:
                return None

        date_departure = date_arrival + timedelta(days=int(days))

        # find existing booking for the given dates
        existing_booking_qs = models.Booking.objects.find_for_period(date_arrival, date_departure)
        if category and int(category):
            existing_booking_qs = existing_booking_qs.filter(room__category__id=int(category))
        if room:
            existing_booking_qs = existing_booking_qs.filter(room__id=room)
        existing_booking_qs = existing_booking_qs.values('room').distinct()

        # find appropriate rooms
        rooms_qs = models.Room.objects.all()
        if category:
            rooms_qs = rooms_qs.filter(category_id=category)
        if room:
            rooms_qs = rooms_qs.filter(pk=room)
        if tenants:
            rooms_qs = rooms_qs.filter(category__places__gte=tenants)

        # we use the simplest algo with strict date bounds by the arrival and departure dates
        closed_rooms_ids = [booking['room'] for booking in existing_booking_qs]

        rooms_qs = rooms_qs.exclude(pk__in=closed_rooms_ids)

        paginator = Paginator(rooms_qs, limit)
        rooms = paginator.get_page(offset)

        open_rooms = []
        for room in rooms:
            open_rooms.append(BookingOption(room, date_arrival, days))

        return {
            'rooms': open_rooms,
            'pages': rooms
        }
