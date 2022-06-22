from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>/settings', views.update_profile, name='update_profile'),
    path('<username>/profile', views.user_profile, name='userprofile'),
    
    
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)