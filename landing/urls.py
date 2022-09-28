from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('privacy', views.internal, name='privacy'),
    path('toc', views.internal, name='toc'),
    path('appoinment', views.internal, name='appoinment'),

    path('rooms', views.rooms, name='rooms'),
    path('categories', views.categories, name='categories'),
    path('testimonial', views.testimonial, name='testimonial'),
]
