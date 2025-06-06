# profileapp/utils.py

from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"http://127.0.0.1:8000{reverse('verify_email', kwargs={'uidb64': uid, 'token': token})}"
    
    subject = "Confirmez votre compte"
    message = f"Bonjour {user.username},\n\nCliquez sur le lien suivant pour confirmer votre adresse email :\n{verification_link}\n\nSi vous n'avez pas demandé cette vérification, ignorez cet email."
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
