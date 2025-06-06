from django.urls import path 
from . import views 

urlpatterns = [ 
 
    path('', views.home_view, name='Home'),
    
    
    path('liste-produits/', views.liste_produits, name='liste_produits'),
        path("liste-categories/", views.liste_categories, name="liste_categories"),

     path('produit/<slug:slug>/', views.produit_detail_view, name='produit_detail'),


] 