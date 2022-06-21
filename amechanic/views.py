from django.shortcuts import render, redirect,  get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    
    return render (request, 'home.html')

@login_required(login_url= '/accounts/login/')
def profile(request, username):

  
    return render(request, 'profile/profile.html')

@login_required(login_url= '/accounts/login/')
def update_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        profileform = ProfileForm(request.POST, request.FILES, instance= request.user.profile)    
        if profileform.is_valid():           
            profileform.save()
        return redirect( 'profile', user.username)
    else:
        profileform = ProfileForm(instance = request.user.profile)
        
    context ={
            "profileform": profileform
    }
    return render(request, "profile/update_profile.html", context)
 
