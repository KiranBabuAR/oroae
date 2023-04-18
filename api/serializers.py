from rest_framework import serializers
from hospitalapp.models import Location, Hospital

"""
LocationSerializer is used to serialize the Location model 
"""

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__' # Serialize all fields

class HospitalSerializer(serializers.ModelSerializer):
    location = LocationSerializer() # Embed the location object in the hospital object

    class Meta:
        model = Hospital
        fields = '__all__' # Serialize all fields
