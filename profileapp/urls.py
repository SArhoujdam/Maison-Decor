from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .models import Profileapp
from . import views
from profileapp.views import login_view, logout_view, register_view, verify_email
from django.conf.urls.static import static
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

# Fonction d'envoi de l'email de vérification


# Configuration des URLs
urlpatterns = [
    
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('register/', views.register_view, name='register'),
      path('login/', login_view, name='login'), 
    

     path('logout/', logout_view, name='home'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
