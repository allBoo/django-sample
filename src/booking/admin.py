from django.contrib import admin
from booking import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    model = models.Category
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    model = models.Room
    list_display = ('number', 'category')
    search_fields = ('number', )
    list_filter = ('category', )


@admin.register(models.Citizenship)
class CitizenshipAdmin(admin.ModelAdmin):
    model = models.Citizenship
    search_fields = ('name',)


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    model = models.Client
    list_display = ('full_name', 'email', 'birth_date', 'citizenship')
    search_fields = ('full_name', 'email', )
    list_filter = ('birth_date', 'citizenship')


class TenantsInline(admin.TabularInline):
    model = models.Tenant
    extra = 0
    min_num = 1


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    model = models.Booking
    list_display = ('room', 'date_arrival', 'date_departure', 'days', 'tenants_count', 'approved')
    list_filter = ('room', )
    inlines = [TenantsInline]
