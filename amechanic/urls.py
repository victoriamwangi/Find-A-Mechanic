from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import contactView, successView


urlpatterns = [
    path('', views.home, name='home'),

    path('profile/<username>', views.profile, name='profile'),

    path('profiles/<username>/profile/', views.show_profile, name='show_profile'),  
    path('profile/<username>/settings', views.update_profile, name='update_profile'),
    path('viewprofile/<username>', views.view_profile, name='viewprofile'),    

    path('contact/', contactView, name='contact'),

    path('success/', successView, name='success'),

    path('aboutus/', views.Aboutus, name='aboutus'),

    path('mechposts/', views.view_post, name='mechpost'),

    path('mechs/', views.mechs, name='mechs'),
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)