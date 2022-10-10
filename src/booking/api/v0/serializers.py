import logging
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError
from booking import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'

    rooms_count = serializers.IntegerField(required=False, allow_null=True, read_only=True)


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Room
        fields = '__all__'

    category = CategorySerializer()
