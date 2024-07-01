from django import forms
from .models import *

class RegionForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = [
            'name', 
        ]

    
class DistrictForm(forms.ModelForm):

    class Meta:
        model = District
        fields = [
            'region',
            'name', 
        ]