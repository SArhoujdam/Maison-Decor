
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from PFE import views 
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

from profileapp.views import login_view

urlpatterns = [
    path('', include('Home.urls')),
    
    path('admin/', admin.site.urls),
    path('Categories/',include('Categories.urls')),
    path('contact_app/', include('contact_app.urls')),  
    path('profileapp/', include('profileapp.urls')),
    path('Home/',include('Home.urls')),
    
    path('promo/',include('promo.urls')),
    path('Sur_cammand/',include('Sur_cammand.urls')),
    path('checkout/', views.checkout, name='checkout'),
    path('Categories_list2/', views.categories_liste2, name='Categories_list2'),
     path('save_redirect_url/', views.save_redirect_url, name='save_redirect_url'),
    path('order-confirmation/<int:commande_id>/', views.order_confirmation, name='order_confirmation'),
    path('download-ticket/<int:commande_id>/', views.download_ticket, name='download_ticket'),
 path('recherche/', views.recherche, name='recherche'),
 path('generate_order_pdf/', views.generate_order_pdf, name='generate_order_pdf'),
path('ajouter_produit_home/', views.ajouter_produit_home, name='ajouter_produit_home'),
path('ajouter_produit_promo/', views.ajouter_produit_promo, name='ajouter_produit_promo'),
     path('get_product_sales_data/<int:product_id>/', views.get_product_sales_data, name='get_product_sales_data'),
      path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
      path('liste_utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('navigation_dashboard/', views.navigation_dashboard, name='navigation_dashboard'),
     path('modifier_utilisateur/<int:user_id>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('supprimer_utilisateur/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('changer_admin/<int:user_id>/', views.changer_admin, name='changer_admin'),
    path('appearance/', views.appearance_view, name='appearance'),
  path('save_appearance/', views.save_appearance, name='save_appearance'),
  path('get_appearance_preferences/', views.get_appearance_preferences, name='get_appearance_preferences'),
   path('commandes_list/',views. liste_commandes, name='commandes_list'),
path('produit_list/', views.produit_list, name='produit_list1'),
 path('ajouter-produit/', views.ajouter_produit, name='ajouter_produit'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),

    # ... autres URLs ...
    
    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
