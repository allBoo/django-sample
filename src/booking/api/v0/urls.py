from django.urls import path
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import views

router = routers.SimpleRouter()

router.register(
    r'categories',
    views.CategoryViewSet,
    basename='booking_api_categories'
)

router.register(
    r'rooms',
    views.RoomViewSet,
    basename='booking_api_room'
)


urlpatterns = [
]

urlpatterns = format_suffix_patterns(router.urls + urlpatterns)
