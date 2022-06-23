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

class ContactForm(forms.Form):
    Name = forms.CharField(required=True)
    Email = forms.EmailField(required=True)
    Subject = forms.CharField(required=True)
    Message = forms.CharField(widget=forms.Textarea, required=True)
    
    
    
# MULTIUSER TEST 
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Mechanic, User

from django.contrib.auth.forms import UserCreationForm
from .models import User

class MechSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_mechanic = True
        if commit:
            user.save()
        return user
    
class OwnerSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=CarModels.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        car_owner = CarModels.objects.create(user=user)
        car_owner.modelcar.add(*self.cleaned_data.get('models'))
        return user
    # add modelcar