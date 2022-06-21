from django import forms 
from .models import *
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("email", "prof_image","bio", "first_name", "second_name", 'location')