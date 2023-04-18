from django import forms
from .models import Hospital
from .models import Location

class HospitalForm(forms.ModelForm):
    """
    HospitalForm is used to create a form for the Hospital model
    """
    class Meta:
        model = Hospital
        fields = ['name', 'beds_available']

class LocationForm(forms.ModelForm):
    """
    LocationForm is used to create a form for the Location model
    """
    class Meta:
        model = Location
        fields = ['name', 'address', 'latitude', 'longitude']

