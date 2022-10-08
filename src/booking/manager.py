from django.db import models
from django.db.models.query import QuerySet, Q
from datetime import datetime


class BookingModelManager(models.Manager):

    def find_room_for_period(self, room, date_arrival: datetime.date, date_departure: datetime.date) -> QuerySet:
        return self.filter(room=room, approved=True).\
            filter(Q(date_arrival__lt=date_departure) & Q(date_departure__gt=date_arrival))
