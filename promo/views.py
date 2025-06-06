import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from Categories.models import Categorie
from .models import promo, Produit
from django.views.decorators.csrf import csrf_exempt
from profileapp.models import Profileapp

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
def is_admin(user):
    return user.is_superuser

###################################
from django.core.paginator import Paginator
from django.shortcuts import render
 # Assurez-vous que c’est bien le nom de votre modèle

def Promo_view(request):
    promos = promo.objects.select_related('produit')

    # Pagination : 10 éléments par page (modifiable selon vos besoins)
    paginator = Paginator(promos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        try:
            profile = Profileapp.objects.get(user=request.user)
        except Profileapp.DoesNotExist:
            profile = None
    else:
        profile = None

    return render(request, 'promo/promo.html', {
        'page_obj': page_obj,
        'promos': promos, 'profile': profile}
    )




def produit_detail_view(request, slug):
    # Vérifie si l'utilisateur est authentifié
    if request.user.is_authenticated:
        try:
            # Récupère le profil de l'utilisateur
            profile = Profileapp.objects.get(user=request.user)
        except Profileapp.DoesNotExist:
            profile = None
    else:
        profile = None

    # Récupère le produit en fonction de son id
   
    produit = get_object_or_404(Produit, slug=slug)
    produits_similaires = Produit.objects.filter(categorie=produit.categorie).exclude(id=produit.id)[:8]

    # Rendu de la page avec le produit et les produits similaires
    return render(request, 'produit_detail.html', {
        'produit': produit,
        'produits_similaires': produits_similaires,
        'profile': profile
    })
###########################################

            # Ajouter ce produit à la promotion



