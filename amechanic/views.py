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

# User's PROFILE
@login_required(login_url= '/accounts/login/')
def profile(request, username):
    return render (request, 'profile/profile.html')

@login_required(login_url='/accounts/login/')
def view_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = current_user
            post.save()
        return redirect('home')

    else:
        form = PostForm()
    return render(request, 'mechposts.html', {"form": form})



@login_required(login_url='/accounts/login/')
def mechs(request):
    post = Post.objects.all()
    return render(request, 'mechs.html',{'post':post})


# VIEW A MECHANIC'S PROFILE-postdetails
@login_required(login_url= '/accounts/login/')
def view_profile(request, id):
    post = Post.objects.get(pk = id)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)    # Create Comment object but don't save to database yet
            new_comment.post = post   # Assign the current post to the comment
            new_comment.save()       # Save the comment to the database
    else:
        comment_form = CommentForm()

    return render(request, 'viewprofile.html',{'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})   
    
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
