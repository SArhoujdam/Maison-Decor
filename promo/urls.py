from django.urls import path
from . import views

urlpatterns = [
    path('', views.Promo_view, name='promo'),
  
    path('produit/<slug:slug>/', views.produit_detail_view, name='produit_detail'),
]