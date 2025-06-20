
import Categories
from profileapp.models import Profileapp
from .models import Home, Produit
from Categories.models import Categorie
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib.auth.views import redirect_to_login
def is_admin(user):
    return user.is_superuser
def home_view(request):
    if request.user.is_authenticated:
        try:
            profile = Profileapp.objects.get(user=request.user)
        except Profileapp.DoesNotExist:
            profile = None
        products = Produit.objects.filter(homes__isnull=False).distinct()
    else:
        profile = None
        products = Produit.objects.filter(homes__isnull=False).distinct()

    categories = Categorie.objects.all()
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'profile': profile,
    }
    return render(request, 'home/home.html', context)
def produit_detail_view(request, slug):
    # Si l'utilisateur n'est pas connecté, redirige vers login avec "next"
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())

    # Si connecté, récupérer son profil
    try:
        profile = Profileapp.objects.get(user=request.user)
    except Profileapp.DoesNotExist:
        profile = None

    # Récupérer le produit demandé
    produit = get_object_or_404(Produit, slug=slug)

    # Récupérer des produits similaires (même catégorie, exclure l’actuel)
    produits_similaires = Produit.objects.filter(
        categorie=produit.categorie
    ).exclude(id=produit.id)[:8]

    # Rendu de la page produit
    return render(request, 'produit_detail.html', {
        'produit': produit,
        'produits_similaires': produits_similaires,
        'profile': profile
    })
@login_required
@user_passes_test(is_admin)


def liste_produits(request):
    produits = list(Produit.objects.values('id', 'nom'))
    return JsonResponse({'produits': produits})

@login_required
@user_passes_test(is_admin)
def liste_categories(request):
    categories = list(Categorie.objects.values('id', 'nom'))
    return JsonResponse({'Categories': categories})

