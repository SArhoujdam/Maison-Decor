from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .utils import send_verification_email
 # Correction de l'import
from .models import Profileapp

# Page d'accueil


# Vue du profil
@login_required
def profile_view(request):
    try:
        profile = Profileapp.objects.get(user=request.user)
    except Profileapp.DoesNotExist:
        messages.error(request, "Aucun profil trouvé.")
        return redirect('edit_profile')

    return render(request, 'profileapp/profile.html', {'profile': profile})

# Modifier le profil
@login_required
def edit_profile_view(request):
    user = request.user
    profile, created = Profileapp.objects.get_or_create(user=user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        profile_image = request.FILES.get('profile_image')

        if username:
            user.username = username
        if email:
            user.email = email
        user.save()

        if profile_image:
            profile.profile_photo = profile_image
            profile.save()

        if password1 and password2:
            if password1 != password2:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return render(request, 'edit_profile.html', {'profile': profile})

            user.set_password(password1)
            user.save()
            messages.success(request, "Votre mot de passe a été mis à jour.")

        messages.success(request, "Votre profil a été mis à jour.")
        return redirect('profile')

    return render(request, 'profileapp/edit_profile.html', {'profile': profile})

# Enregistrement avec email de vérification
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if not all([username, email, password1, password2]):
            messages.error(request, 'Veuillez remplir tous les champs.')
            return render(request, 'profileapp/register_page.html')

        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'profileapp/register_page.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d’utilisateur existe déjà.')
            return render(request, 'profileapp/register_page.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Cette adresse email est déjà utilisée.')
            return render(request, 'profileapp/register_page.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_active = False
        user.save()

        send_verification_email(user)

        messages.success(request, 'Compte créé avec succès ! Vérifiez votre email pour l’activer.')
        return redirect('login')

    return render(request, 'profileapp/register_page.html')



# Vérification de l'email
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a été activé avec succès ! Vous pouvez maintenant vous connecter.")
        return redirect('login')
    else:
        messages.error(request, "Le lien de vérification est invalide ou a expiré.")
        return redirect('Home')



# Connexion

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)

            redirect_url = request.session.pop('redirect_after_login', None)
            if redirect_url:
                return redirect(redirect_url)
            elif user.is_staff:
                return redirect('commandes_list')
            else:
                return redirect('Home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('login')

    return render(request, 'profileapp/login_page.html')































# Déconnexion

def logout_view(request):
    logout(request)
    return redirect('Home')