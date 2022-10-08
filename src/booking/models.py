from django.db import models
from .manager import BookingModelManager


class Category(models.Model):

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=256, help_text="the name of the category", blank=False, null=False, unique=True)
    thumbnail = models.ImageField(upload_to='categories', null=True, blank=True, help_text='Thumbnail image')
    square = models.PositiveSmallIntegerField(blank=False, null=False)
    places = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    price = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

    @property
    def rooms_count(self):
        """ @note - be careful with N+1 """
        return self.rooms.count()


class Room(models.Model):

    class Meta:
        ordering = ('number',)

    number = models.CharField(max_length=20, blank=False, null=False, unique=True)
    thumbnail = models.ImageField(upload_to='rooms', null=True, blank=True, help_text='Thumbnail image')
    category = models.ForeignKey(Category, blank=False, null=False, related_name='rooms', on_delete=models.RESTRICT)

    def __str__(self):
        return self.number


class Citizenship(models.Model):

    class Meta:
        ordering = ('name',)

    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Client(models.Model):

    email = models.EmailField(blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=256, blank=False, null=False)
    birth_date = models.DateField(blank=True, null=True)
    citizenship = models.ForeignKey(Citizenship, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.full_name


class Booking(models.Model):

    room = models.ForeignKey(Room, blank=False, null=False, on_delete=models.RESTRICT)
    date_arrival = models.DateField(blank=False, null=False)
    date_departure = models.DateField(blank=False, null=False)
    approved = models.BooleanField(default=False)

    objects = BookingModelManager()

    def __str__(self):
        return '%s from %s till %s' % (self.room, self.date_arrival, self.date_departure)

    @property
    def days(self):
        return (self.date_departure - self.date_arrival).days

    @property
    def tenants_count(self):
        return self.tenants.count()

    def clean(self):
        from .validators import BookingValidator

        BookingValidator().validate(self)

        return super(Booking, self).clean()


class Tenant(models.Model):

    booking = models.ForeignKey(Booking, blank=False, null=False, on_delete=models.RESTRICT, related_name='tenants')
    client = models.ForeignKey(Client, blank=False, null=False, on_delete=models.RESTRICT, related_name='bookings')
