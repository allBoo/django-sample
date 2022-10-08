from . import models
from django.core.exceptions import ValidationError


class BookingValidator:

    def __init__(self):
        pass

    def validate(self, booking: models.Booking):
        self._check_interval_correct(booking)
        self._check_dates_busy(booking)

    def _check_interval_correct(self, booking: models.Booking):
        errors = {}

        if not booking.date_arrival:
            errors['date_arrival'] = 'The Arrival Date can not be empty'

        if not booking.date_departure:
            errors['date_departure'] = 'The Departure Date can not be empty'

        if booking.date_departure <= booking.date_arrival:
            errors['date_departure'] = 'The Departure Date must be greater than the Arrival Date'

        if errors:
            raise ValidationError(errors)

    def _check_dates_busy(self, booking: models.Booking):
        if not booking.approved:
            return

        exists_booking = models.Booking.objects.find_room_for_period(booking.room, booking.date_arrival, booking.date_departure)

        if booking.id:
            exists_booking = exists_booking.exclude(pk=booking.id)

        print(exists_booking.first())
        if exists_booking.first():
            raise ValidationError('The room is already booked for given dates')
