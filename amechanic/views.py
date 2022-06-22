from django.shortcuts import render, redirect,  get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    return render (request, 'home.html')


@login_required(login_url= '/accounts/login/')
def profile(request, username):
    user = User.objects.get(username=username)
    ratings = Rating.objects.filter(user=request.user, profile=user).first()
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
    return render(request, 'profile/profile.html', params)
    

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

def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, 'userprofile.html', params)
 
