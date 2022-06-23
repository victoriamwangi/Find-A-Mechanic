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
    Message = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':35,}), required=True)

    
class PostForm(forms.ModelForm):
     class Meta:
        model = Post
        fields = ("name", "image","description", "carmodel", "location", "contact")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
          'body': forms.Textarea(attrs={'rows':3, 'cols':25,}),
        }
