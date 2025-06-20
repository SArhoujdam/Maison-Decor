from django.urls import path
from django.conf.urls.static import static
from PFE import settings
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.liste_categories, name='categories_list'),
    path('add/', views.ajouter_categorie, name='ajouter_Categorie'),
    path('edit/<int:pk>/', views.modifier_categorie, name='category_edit'),
    path('delete/<int:pk>/', views.supprimer_categorie, name='supprimer_categorie'),
    path('categorie/<slug:slug>/produits/', views.produits_par_categorie, name='produits_par_categorie'),
    path('categorie/<slug:slug>/', views.produits_par_categorie, name='single_categorie'),
    path('produit/supprimer/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
     path('produit/<slug:slug>/', views.produit_detail_view, name='produit_detail'),

    path('produit_list/', views.produit_list, name='produit_list'),
    path('recherche_produit/', views.recherche_produit, name='recherche_produit'),
    path('<slug:slug>/', views.afficher_produits, name='produits_par_categorie'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
