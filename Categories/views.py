from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from profileapp.models import Profileapp
from .models import Categorie, Produit
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
def is_admin(user):
    return user.is_superuser

def liste_categories(request, slug): 
    if request.user.is_authenticated:
        categories = Categorie.objects.all()
        try:
            profile = Profileapp.objects.get(user=request.user)
        except Profileapp.DoesNotExist:
            profile = None
    else:
        categories = Categorie.objects.all()
        profile = None
    
    return render(request, 'categories/Categories.html', {'categories': categories, 'profile': profile})


@user_passes_test(lambda u: u.is_superuser)
@login_required
def ajouter_categorie(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        photo = request.FILES.get('photo')
        if nom and photo:
            Categorie.objects.create(nom=nom, photo=photo)
            messages.success(request, "Catégorie ajoutée avec succès.")
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
        return redirect('Categories_list2')
    return render(request, 'PFE/Categories_list.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def modifier_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == "POST":
        nom = request.POST.get('nom')
        photo = request.FILES.get('photo')
        if nom:
            categorie.nom = nom
        if photo:
            categorie.photo = photo
        categorie.save()
        messages.success(request, "Catégorie modifiée avec succès.")
        return redirect('Categories_list2')
    return render(request, 'PFE/Categories_list.html', {'categorie': categorie})
@login_required
@user_passes_test(lambda u: u.is_superuser)
def supprimer_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == "POST":
        categorie.delete()
        messages.success(request, "Catégorie supprimée avec succès.")
        return redirect('Categories_list2')
    return render(request, 'PFE/Categories_list.html')
def produits_par_categorie(request, slug):
    categorie = get_object_or_404(Categorie, slug=slug)
    produits = Produit.objects.filter(categorie=categorie)
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profileapp.objects.get(user=request.user)
        except Profileapp.DoesNotExist:
            pass
    return render(request, 'categories\produits_par_categorie.html', {
        'categorie': categorie,
        'produits': produits,
        'profile': profile,
    })

from django.shortcuts import render, get_object_or_404
from .models import Produit

def produit_detail_view(request, slug):
    produit = get_object_or_404(Produit, slug=slug)
    produits_similaires = Produit.objects.filter(categorie=produit.categorie).exclude(id=produit.id)[:8]

    return render(request, 'produit_detail.html', {
        'produit': produit,
        'produits_similaires': produits_similaires,
    })





def afficher_produits(request, slug):

    categorie = get_object_or_404(Categorie, slug=slug)

   
    produits = Produit.objects.filter(categorie=categorie)

    
    profile = None

   
    if request.user.is_authenticated:
        try:
            
            profile = Profileapp.objects.get(user=request.user)
        except Profileapp.DoesNotExist:
            
            pass

    return render(request, 'categories\produits_par_categorie.html', {
        'categorie': categorie,
        'produits': produits,
        'profile': profile,
    })


# إضافة منتج
@login_required
@user_passes_test(lambda u: u.is_superuser)

# تعديل منتج
@login_required
@user_passes_test(lambda u: u.is_superuser)




# حذف منتج
@login_required
@user_passes_test(lambda u: u.is_superuser)
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        produit.delete()
        return redirect('categories:produits_par_categorie', categorie_id=produit.categorie_id)
    return render(request, 'categories/produits_par_categorie.html', {'produit': produit})
def produit_list(request):
    produits = Produit.objects.all()
    return render(request, 'categories/liste_produits.html', {'produits': produits})




def recherche_produit(request):
    recherche_produit = request.GET.get('recherche')
    
    if recherche_produit:
        produits = Produit.objects.filter(nom__icontains=recherche_produit)
    else:
        produits = Produit.objects.all()

    categories = Categorie.objects.all()
    
    paginator = Paginator(produits, 1)
    page = request.GET.get('page')
    produits = paginator.get_page(page)

    return render(request, 'categories/liste_produits.html', {
        'produits': produits,
        'categories': categories,
        'recherche': recherche_produit
    })
