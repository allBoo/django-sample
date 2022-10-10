from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('privacy', views.internal, name='privacy'),
    path('toc', views.internal, name='toc'),
    path('appointment', views.appointment, name='appointment'),

    path('rooms', views.rooms, name='rooms'),
    re_path(r'rooms/(?P<id>\d+)', views.room_details, name='room_details'),
    path('categories', views.categories, name='categories'),
    path('testimonial', views.testimonial, name='testimonial'),
]
