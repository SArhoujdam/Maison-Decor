from decimal import Decimal
from email.headerregistry import Address
import json
import profile
from pyexpat.errors import messages
import qrcode
from io import BytesIO
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tempfile import NamedTemporaryFile
from django.db.models import Count, Sum
from .models import Commande, LigneCommande, UserAppearancePreferences
from profileapp.models import Profileapp
from Categories.models import Categorie, Produit
from PFE.models import Commande as PFECommande
from Home.models import Home 
from django.db.models import Sum, Prefetch
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User



from promo.models import promo 
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def is_admin(user):
    return user.is_staff or user.is_superuser
@login_required
@user_passes_test(is_admin)
def produit_list(request):
    profile = Profileapp.objects.get(user=request.user)
   
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
   
    home_products = Produit.objects.filter(homes__isnull=False).distinct()
    promo_products = Produit.objects.filter(promos__isnull=False).distinct()
    


    
    paginator = Paginator(produits, 9) 
    page_number = request.GET.get('page')
    produits_page = paginator.get_page(page_number)  

    return render(request, 'PFE/liste_produits.html', {
        'produits': produits_page,  
        'home_products': home_products, 
         'promo_products': promo_products,
           'categories': categories,
             'profile':profile, 
    })

@login_required
@user_passes_test(is_admin)
def liste_utilisateurs(request):
    profile = Profileapp.objects.get(user=request.user)
    utilisateurs = User.objects.all()
    return render(request, 'utilisateur.html', {'utilisateurs': utilisateurs,'profile': profile})

@login_required
@user_passes_test(is_admin)
def navigation_dashboard(request):
 
    profile = Profileapp.objects.get(user=request.user)

    context = {'profile': profile}
    return render(request, 'pages.html', context)
@login_required
@user_passes_test(is_admin)
def changer_admin(request, user_id):
    if request.method == 'POST':
        try:
            utilisateur = User.objects.get(pk=user_id)
            utilisateur.is_staff = not utilisateur.is_staff
            utilisateur.save()
            return JsonResponse({'success': True, 'is_staff': utilisateur.is_staff})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Utilisateur introuvable'})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})
@login_required
@user_passes_test(is_admin)
def supprimer_utilisateur(request, user_id):
    if request.method == 'DELETE':
        try:
            utilisateur = User.objects.get(pk=user_id)
            utilisateur.delete()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Utilisateur introuvable'})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})
@login_required
@user_passes_test(is_admin)
def modifier_utilisateur(request, user_id):
    if request.method == 'POST':
        try:
            utilisateur = User.objects.get(pk=user_id)
            utilisateur.username = request.POST.get('username')
            utilisateur.email = request.POST.get('email')
            utilisateur.first_name = request.POST.get('first_name')
            utilisateur.last_name = request.POST.get('last_name')
            utilisateur.password = request.POST.get('password')
            utilisateur.save()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Utilisateur introuvable'})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})
@login_required
def checkout(request):
    profile = Profileapp.objects.get(user=request.user)
    nom_produit = request.GET.get('nom')
    prix_produit = request.GET.get('prix')
    photo_url = request.GET.get('photo')
    if not nom_produit or not prix_produit or not photo_url:
        return HttpResponseBadRequest("Les informations du produit sont manquantes.")
    payment_method = None
    if request.method == 'POST':
        adresse_livraison = request.POST.get('adresse')
        quantite = int(request.POST.get('quantite'))
        produits = Produit.objects.filter(nom=nom_produit)
        if not produits.exists():
            return HttpResponseBadRequest("Produit non trouvé.")
        produit = produits.first()
        if produit.quantite < quantite:
            return HttpResponseBadRequest("Quantité demandée non disponible en stock.")
        payment_method = request.POST.get('payment_method')
        if payment_method not in ['credit_card', 'paypal', 'cod']:
            return HttpResponseBadRequest("Méthode de paiement non valide.")
        commande = Commande.objects.create(
            user=request.user,
            adresse_livraison=adresse_livraison,
            quantite=quantite,
            Methode_paiement=payment_method,
        )
        commande.produits.add(produit)
        produit.quantite -= quantite
        produit.save()
        return redirect('order_confirmation', commande_id=commande.id)
    context = {
        'nom_produit': nom_produit,
        'prix_produit': prix_produit,
        'photo_url': photo_url,
        'payment_method': payment_method,
        'profile': profile,}
    return render(request, 'checkout.html', context)
@login_required
@login_required


def order_confirmation(request, commande_id):
    profile = Profileapp.objects.get(user=request.user)
    commande = get_object_or_404(Commande, id=commande_id, user=request.user)

   
    lignes_commande = LigneCommande.objects.filter(commande=commande)

   
    produit = lignes_commande.first().produit if lignes_commande.exists() else None

    context = {
        'profile': profile,
        'commande': commande,
        'produit': produit,
        'lignes_commande': lignes_commande,
        'download_pdf_url': f"/download-ticket/{commande.id}/",
    }
    return render(request, 'order_confirmation.html', context)
@login_required
@login_required
def generate_order_pdf(commande, lignes_commande):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Billet d'achat")

    p.setFont("Helvetica", 12)
    y = 720
    p.drawString(100, y, f"Commande ID: {commande.id}")
    y -= 20
    p.drawString(100, y, f"Utilisateur: {commande.user.username}")
    y -= 20
    p.drawString(100, y, f"Adresse de livraison: {commande.adresse_livraison}")
    y -= 20
    p.drawString(100, y, f"Date: {commande.created_at.strftime('%d/%m/%Y %H:%M')}")

    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "Produits :")
    y -= 20
    p.setFont("Helvetica", 11)

    for ligne in lignes_commande:
        p.drawString(100, y, f"- {ligne.produit.nom} : {ligne.quantite} x {ligne.prix_unitaire} DHs")
        y -= 20

    p.drawString(100, y, f"Total : {commande.prix_total} Dhs")

    # QR Code
    qr_code_data = f"/download-ticket/{commande.id}/"
    qr_code_img = qrcode.make(qr_code_data)
    with NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        qr_code_img.save(temp_file, 'PNG')
        temp_file.seek(0)
        p.drawImage(temp_file.name, 400, 600, width=100, height=100)

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
def update_quantity(request, produit_id):
    if request.method == 'POST':
        qty = int(request.POST.get('qty', 1))
        panier = request.session.get('cart', {})
        if str(produit_id) in panier:
            panier[str(produit_id)] = {'qty': qty}
            request.session['cart'] = panier
    return redirect('cart')

@login_required

@login_required
def download_ticket(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, user=request.user)

    
    lignes_commande = LigneCommande.objects.filter(commande=commande)

    if not lignes_commande.exists():
        return HttpResponseBadRequest("Aucun produit trouvé pour cette commande.")
    pdf_buffer = generate_order_pdf(commande, lignes_commande)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="billet_achat_{commande.id}.pdf"'
    response.write(pdf_buffer.getvalue())
    return response

@login_required
@user_passes_test(is_admin)
def get_appearance_preferences(request):
    try:
        preferences = UserAppearancePreferences.objects.get(user=request.user)
        return JsonResponse({
            'background_color': preferences.background_color,
            'text_color': preferences.text_color,
            'font_family': preferences.font_family,
        })
    except UserAppearancePreferences.DoesNotExist:
        return JsonResponse({
            'background_color': '#ffffff',
            'text_color': '#000000',
            'font_family': 'sans-serif',
        })
@login_required
@user_passes_test(is_admin)
def get_user_preferences(request):
    
    try:
        preferences = UserAppearancePreferences.objects.get(user=request.user)
        return {
            'background_color': preferences.background_color,
            'text_color': preferences.text_color,
            'font_family': preferences.font_family,
        }
    except UserAppearancePreferences.DoesNotExist:
        return {
            'background_color': '#ffffff',
            'text_color': '#000000',
            'font_family': 'sans-serif',
            
        }

@login_required
@user_passes_test(is_admin)
def appearance_view(request):
    profile = Profileapp.objects.get(user=request.user)
    preferences = get_user_preferences(request)
    context = {
        'profile': profile,
        'background_color': preferences['background_color'],
        'text_color': preferences['text_color'],
        'font_family': preferences['font_family'],
    }
    return render(request, 'appearance.html', context)


@login_required
@user_passes_test(is_admin)
def save_appearance(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            background_color = data['backgroundColor']
            text_color = data['textColor']
            font_family = data['fontFamily']

            preferences, created = UserAppearancePreferences.objects.update_or_create(
                user=request.user,
                defaults={
                    'background_color': background_color,
                    'text_color': text_color,
                    'font_family': font_family,
                },
            )

            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

@login_required
@staff_member_required
@login_required
@staff_member_required

def liste_commandes(request):
    utilisateurs = User.objects.all()
    profile = Profileapp.objects.get(user=request.user)

    # Préchargement des relations pour optimiser les requêtes
    commandes = Commande.objects.select_related('user').prefetch_related(
        Prefetch('lignecommande_set', queryset=LigneCommande.objects.select_related('produit'))
    ).all()

    # Mode debug : afficher les produits de chaque commande
    if 'debug' in request.GET:
        debug_data = []
        for c in commandes:
            produits = [lc.produit.nom for lc in c.lignecommande_set.all()]
            debug_data.append(f"ID:{c.id} | User:{c.user.username} | Produits:{produits}")
        return HttpResponse("<br>".join(debug_data))

    # Agréger les données par utilisateur
    utilisateurs_data = {}
    for commande in commandes:
        utilisateur = commande.user.username
        quantite = sum(lc.quantite for lc in commande.lignecommande_set.all())  # ✅ Correction ici
        adresse = commande.adresse_livraison

        if utilisateur not in utilisateurs_data:
            utilisateurs_data[utilisateur] = {
                'quantite_totale': quantite,
                'adresse_livraison': adresse
            }
        else:
            utilisateurs_data[utilisateur]['quantite_totale'] += quantite

    total_utilisateurs = len(utilisateurs_data)
    total_utilisateurs_str = f"{total_utilisateurs} utilisateurs"

    # Total des produits vendus
    total_produits_vendus = LigneCommande.objects.aggregate(
        total=Sum('quantite')
    )['total'] or 0

    # Produits les plus vendus (Top 5)
    produits_vendus = (
        LigneCommande.objects
        .values('produit__nom')
        .annotate(total_vendu=Sum('quantite'))
        .order_by('-total_vendu')[:5]
    )

    # Format des données pour Chart.js ou autres
    produits_vendus = [
        {
            'produit': {'nom': p['produit__nom']},
            'total_vendu': p['total_vendu']
        }
        for p in produits_vendus
    ]

    return render(request, 'PFE/dashboard.html', {
        'profile': profile,
        'utilisateurs': utilisateurs,
        'commandes_par_utilisateur': utilisateurs_data,
        'total_utilisateurs': total_utilisateurs_str,
        'total_produits_vendus': total_produits_vendus,
        'produits_vendus': produits_vendus,
        'commandes': commandes,
        'total': commandes.count()
    })

















@csrf_exempt  # تأكد أنك ترسل الـ CSRF من الجهة الأمامية
def save_redirect_url(request):
    if request.method == "POST":
        data = json.loads(request.body)
        url = data.get("url")
        if url:
            request.session['redirect_after_login'] = url
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)







@login_required
@user_passes_test(is_admin)
def produits_vendus(request):
   
    produits_vendus = Produit.objects.annotate(total_vendu=Count('commandes_PFE')).order_by('-total_vendu')

    
    context = {
        'produits_vendus': produits_vendus,
    }

    return render(request, 'produits_vendus.html', context)
def get_product_sales_data(request, product_id):
    produit = get_object_or_404(Produit, id=product_id)
    
    ventes = Commande.objects.filter(produits=produit)

   
    sales_data = []
    for month in range(1, 13):  
        sales_data.append(ventes.filter(date__month=month).count())

    return JsonResponse({
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'sales': sales_data,
    })








@login_required
@user_passes_test(is_admin)
def ajouter_produit(request):
    categories = Categorie.objects.all() 
    produits = Produit.objects.all()  
    
    if request.method == 'GET':
        return render(request, 'PFE/liste_produits.html', {
            'categories': categories,  
            'produits': produits
             
        })

    elif request.method == 'POST':
        try:
            
            nom = request.POST.get('nom')
            categorie_id = request.POST.get('categorie_id')
            prix = request.POST.get('prix')
            description = request.POST.get('description')
            quantite = request.POST.get('quantite')
            photo = request.FILES.get('photo')

            if not nom or not prix or not quantite or not photo:
                return render(request, 'PFE/liste_produits.html', {
                    'categories': categories,
                    'produits': produits,
                    'erreur': "Tous les champs sont obligatoires."
                })

            categorie = Categorie.objects.get(id=categorie_id)

            produit = Produit.objects.create(
                nom=nom,
                categorie=categorie,
                prix=prix,
                description=description,
                quantite=quantite,
                photo=photo,
                user=request.user  # Assurez-vous que l'utilisateur est lié au produit
            )

            return redirect('produit_list1')  

        except Exception as e:
            print("Erreur:", e)
            return render(request, 'PFE/liste_produits.html', {
                'categories': categories,
                'produits': produits,
                'erreur': "Une erreur est survenue. Vérifiez les données."
            })


@login_required
@user_passes_test(is_admin)
def delete_product(request, product_id):
    try:
        produit = Produit.objects.get(id=product_id)
        produit.delete()
        return redirect('produit_list1')
    except Produit.DoesNotExist:
        return HttpResponse("Produit non trouvé", status=404)


@login_required
@user_passes_test(is_admin)
def edit_product(request, product_id):
    produit = get_object_or_404(Produit, id=product_id)
    profile = Profileapp.objects.get(user=request.user)
    if request.method == 'POST':
        categorie_id = request.POST.get('categorie')
        if not categorie_id:
            return HttpResponse("La catégorie est obligatoire", status=400)

        try:
            categorie = Categorie.objects.get(id=categorie_id)
        except Categorie.DoesNotExist:
            return HttpResponse("Catégorie non trouvée", status=404)

        produit.nom = request.POST.get('nom')
        produit.prix = request.POST.get('prix')
        produit.description = request.POST.get('description')
        produit.quantite = request.POST.get('quantite')
        produit.categorie = categorie
        user = request.user  # Assurez-vous que l'utilisateur est lié au produit

        if 'photo' in request.FILES:
            produit.photo = request.FILES['photo']

        produit.save()
        return redirect('produit_list1')

    else:
      
        categories = Categorie.objects.all()
        return render(request, 'PFE/edit_product.html', {
            'produit': produit,
            'categories': categories,
            'profile': profile,
        })


from django.db.models import Q 

def recherche(request):
    
    if request.user.is_authenticated:
        try:
            
            profile = Profileapp.objects.get(user=request.user)
        except Profileapp.DoesNotExist:
            profile = None
    else:
        profile = None

    recherche_produit = request.GET.get('recherche', '').strip()

  
    if recherche_produit:
        produits = Produit.objects.filter(
            Q(nom__icontains=recherche_produit) |
            Q(categorie__nom__icontains=recherche_produit) |
            Q(prix__icontains=recherche_produit)
        )
    else:
        produits = Produit.objects.all()

    categories = Categorie.objects.all()

    paginator = Paginator(produits, 6)  
    page = request.GET.get('page')
    produits = paginator.get_page(page)

    return render(request, 'categories/produits_par_categorie.html', {
        'produits': produits,
        'categories': categories,
        'recherche': recherche_produit,
        'profile': profile,
    })


@login_required
@user_passes_test(is_admin)
def liste_categories(request):
    profile = Profileapp.objects.get(user=request.user)
    categories = list(Categorie.objects.values('id', 'nom'))
    return JsonResponse({'Categories': categories,'profile': profile})
@login_required
@user_passes_test(is_admin)
def categories_liste2(request):
    categories = Categorie.objects.all()
    profile = Profileapp.objects.get(user=request.user)
    return render(request, 'PFE/Categories_list.html', {'categories': categories,'profile': profile})
@login_required
def ajouter_produit_home(request):
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        methode = request.POST.get('methode')

        if not produit_id or not methode:
            return JsonResponse({'error': 'Requête invalide.'})

        try:
            produit = Produit.objects.get(id=produit_id)
        except Produit.DoesNotExist:
            return JsonResponse({'error': 'Produit introuvable.'})

        if methode == 'ajouter':
            Home.objects.get_or_create(produit=produit)
            message = 'Produit ajouté à Home.'
        elif methode == 'supprimer':
            Home.objects.filter(produit=produit).delete()
            message = 'Produit supprimé de Home.'
        else:
            return JsonResponse({'error': 'Méthode non reconnue.'})

        # Retourner les produits existants dans Home
        produits_home = Home.objects.select_related('produit').all()
        produits_liste = [{
            'id': item.produit.id,
            'nom': item.produit.nom,  # تأكد أن حقل 'nom' كاين فـ modèle Produit
            'prix': item.produit.prix,  # أو أي حقل بغيت تعرضه
        } for item in produits_home]

        return JsonResponse({
            'message': message,
            'produits_home': produits_liste
        })

    return JsonResponse({'error': 'Requête invalide.'})
def ajouter_produit_promo(request):
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        methode = request.POST.get('methode')

        if not produit_id or not methode:
            return JsonResponse({'error': 'Requête invalide.'})

        try:
            produit = Produit.objects.get(id=produit_id)
        except Produit.DoesNotExist:
            return JsonResponse({'error': 'Produit introuvable.'})

        if methode == 'ajouter':
            promo.objects.get_or_create(produit=produit)
            message = 'Produit ajouté à promo.'
        elif methode == 'supprimer':
            promo.objects.filter(produit=produit).delete()
            message = 'Produit supprimé de promo.'
        else:
            return JsonResponse({'error': 'Méthode non reconnue.'})

 
        produits_promo = promo.objects.select_related('produit').all()
        produits_liste = [{
            'id': item.produit.id,
            'nom': item.produit.nom,  # تأكد أن حقل 'nom' كاين فـ modèle Produit
            'prix': item.produit.prix,  # أو أي حقل بغيت تعرضه
        } for item in produits_promo]

        return JsonResponse({
            'message': message,
            'produits_home': produits_liste
        })

    return JsonResponse({'error': 'Requête invalide.'})
from django.core.mail import send_mail



def save(self, *args, **kwargs):
        
        if self.pk: 
            original = Produit.objects.get(pk=self.pk)
            if original.quantite > 2 and self.quantite == 3:
                send_mail(
                    subject='Alerte stock faible',
                    message=f'Le produit "{self.nom}" atteint une quantité de 2 en stock.',
                    from_email=None, 
                    recipient_list=['Sarhoujdam@gmail.com'],
                    fail_silently=False,
                )
        super().save(*args, **kwargs)


def about(request):
    profile = Profileapp.objects.get(user=request.user)
    return render(request, 'about.html', {'profile': profile})
from django.shortcuts import get_object_or_404, redirect
from .models import Produit  # votre modèle
from django.contrib.auth.decorators import login_required

@login_required
  # adapte selon ton app
def add_to_cart(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    # Vérifie s’il y a une promo liée
    has_promo = promo.objects.filter(produit=produit).exists()

    if produit.quantite <= 0 and has_promo:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Produit en promo non disponible ❌'})
        else:
            messages.error(request, "Ce produit en promotion est en rupture de stock.")
            return redirect('cart_view')

    # Continue normalement si disponible
    cart = request.session.get('cart', {})
    produit_id_str = str(produit.id)
    cart[produit_id_str] = cart.get(produit_id_str, 0) + 1
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Produit ajouté avec succès ✅'})
    else:
        return redirect('cart_view')
 # nommez cette URL selon votre config
@login_required





def remove_from_cart(request, produit_id):
    panier = request.session.get('cart', {})
    pid = str(produit_id)
    if pid in panier:
        del panier[pid]
        request.session['cart'] = panier
        request.session.modified = True
    return redirect('cart_view')  # سيُعيد عرض cart_view مع total مُحدّث


# assurez-vous d'avoir le middleware de sessions activé (par défaut) :contentReference[oaicite:3]{index=3}

@login_required(login_url='login')
def cart_view(request):
    profile = Profileapp.objects.get(user=request.user)
    
    if 'cart' not in request.session:
        request.session['cart'] = {}

    panier = request.session['cart']
    produits = []
    total = Decimal('0')

    for pid, data in panier.items():
        produit = get_object_or_404(Produit, id=int(pid))

        # Récupérer la quantité
        qty = int(data.get('qty')) if isinstance(data, dict) else int(data)

        # Limiter au stock disponible
        if produit.quantite < qty:
            qty = produit.quantite

        subtotal = produit.prix * qty
        total += subtotal

        produits.append({
            'produit': produit,
            'qty': qty,
            'subtotal': subtotal,
        })

    # Si formulaire soumis
    if request.method == 'POST':
        adresse = request.POST.get('adresse')
        methode_paiement = request.POST.get('payment_method')

        if not adresse or not methode_paiement:
            messages.error(request, "Veuillez remplir tous les champs requis.")
            return redirect('cart')

        commande = Commande.objects.create(
            user=request.user,
            adresse_livraison=adresse,
            Methode_paiement=methode_paiement,
            prix_total=0  # Temporaire
        )

        prix_total_commande = Decimal('0')

        for item in produits:
            produit = item['produit']
            quantite = item['qty']

            LigneCommande.objects.create(
                commande=commande,
                produit=produit,
                quantite=quantite,
                prix_unitaire=produit.prix
            )

            produit.quantite -= quantite
            produit.save()

            prix_total_commande += produit.prix * quantite

        commande.prix_total = prix_total_commande
        commande.save()

        # Vider le panier
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_confirmation', commande_id=commande.id)

    return render(request, 'cart.html', {
        'produits': produits,
        'total': total,
        'profile': profile,
    })

def checkout(request):
    profile = Profileapp.objects.get(user=request.user)
    nom_produit = request.GET.get('nom')
    prix_produit = request.GET.get('prix')
    photo_url = request.GET.get('photo')

    if not nom_produit or not prix_produit or not photo_url:
        return HttpResponseBadRequest("Les informations du produit sont manquantes.")

    payment_method = None

    if request.method == 'POST':
        adresse_livraison = request.POST.get('adresse')
        quantite = int(request.POST.get('quantite'))
        produits = Produit.objects.filter(nom=nom_produit)

        if not produits.exists():
            return HttpResponseBadRequest("Produit non trouvé.")

        produit = produits.first()

        if produit.quantite < quantite:
            return render(request, 'checkout.html', {
                'error': "La quantité demandée dépasse le stock disponible.",
                'nom_produit': nom_produit,
                'prix_produit': prix_produit,
                'photo_url': photo_url,
                'profile': profile,
            })

        payment_method = request.POST.get('payment_method')
        if payment_method not in ['credit_card', 'paypal', 'cod']:
            return HttpResponseBadRequest("Méthode de paiement non valide.")

        commande = Commande.objects.create(
            user=request.user,
            adresse_livraison=adresse_livraison,
            Methode_paiement=payment_method,
        )

        LigneCommande.objects.create(
            commande=commande,
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix
        )

        produit.quantite -= quantite
        produit.save()

        commande.prix_total = quantite * produit.prix
        commande.save()

        return redirect('order_confirmation', commande_id=commande.id)

    context = {
        'nom_produit': nom_produit,
        'prix_produit': prix_produit,
        'photo_url': photo_url,
        'payment_method': payment_method,
        'profile': profile,
    }

    return render(request, 'checkout.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def add_to_cart(request, produit_id):
    cart = request.session.get('cart', {})
    pid = str(produit_id)
    cart[pid] = cart.get(pid, {'qty': 0})
    cart[pid]['qty'] += 1
    request.session['cart'] = cart
    request.session.modified = True
    return JsonResponse({'status': 'success'})

