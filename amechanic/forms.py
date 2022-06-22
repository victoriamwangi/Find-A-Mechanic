from django import forms 
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("email", "prof_image","bio", "first_name", "second_name", 'location')

class RatingsForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['quality_of_work', 'punctuality', 'customer_relations']

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')