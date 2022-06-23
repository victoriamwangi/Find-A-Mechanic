from django.shortcuts import render, redirect,  get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def home(request):
    return render (request, 'home.html')

def Aboutus(request):
    return render (request, 'aboutus.html')

# MECH'S PROFILE
@login_required(login_url= '/accounts/login/')
def profile(request, username):
    
    return render (request, 'profile/profile.html')

# VIEW A MECHANIC'S PROFILE
@login_required(login_url= '/accounts/login/')
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    rate = Rating.objects.filter(user = user)
    ratings = Rating.objects.all()
    rating_status = None    
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.profile = profile
            rate.save()
            profile_ratings = Rating.objects.filter(profile=profile)

            quality_of_work_ratings = [d.quality_of_work for d in profile_ratings]
            quality_of_work_average = sum(quality_of_work_ratings) / len(quality_of_work_ratings)

            punctuality_ratings = [us.punctuality for us in profile_ratings]
            punctuality_average = sum(punctuality_ratings) / len(punctuality_ratings)

            customer_relations_ratings = [customer_relations.customer_relations for customer_relations in profile_ratings]
            customer_relations_average = sum(customer_relations_ratings) / len(customer_relations_ratings)

            score = (quality_of_work_average + punctuality_average + customer_relations_average) / 3
            print(score)
            rate.design_average = round(quality_of_work_average, 2)
            rate.usability_average = round(punctuality_average, 2)
            rate.content_average = round(customer_relations_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingsForm()
    params = {
        'profile': profile,
        'rating_form': form,
        'rating_status': rating_status
    }
    return render(request, 'profile/viewprofile.html', params)
    
# UPDATE MECH'S PROFILE
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
 


def show_profile(request, username):    
    user = get_object_or_404(User, username=username)
    context = {
        "user": user, 
    }

    
    return render(request, 'profile/user_profile.html', context)

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contacts.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')
