# serializers.py
from rest_framework import serializers
from .models import Landmark


class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = [
            'id',
            'user',
            'name',
            'location_name',
            'description',
            'image',
            'map_location',
            'level',
            'created_at',
            'updated_at',
        ]
