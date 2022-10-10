from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.response import Response
from booking import models
from .pagination import DefaultPagePagination
from . import serializers


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = DefaultPagePagination


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    pagination_class = DefaultPagePagination


