from django.utils import timezone 
from django.contrib.auth.models import User
from Categories.models import Produit
from django.db import models

class Commande(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes_PFE')
    produits = models.ManyToManyField(Produit, related_name='commandes_PFE')
    date_commande = models.DateTimeField(auto_now_add=True)
    adresse_livraison = models.TextField()
    quantite = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    Methode_paiement = models.CharField(max_length=50, default='Carte de crédit')

    def __str__(self):
        return f"Commande #{self.id} par {self.user.username}"
    


class UserAppearancePreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#000000')
    font_family = models.CharField(max_length=50, default='sans-serif')

    def __str__(self):
        return f"{self.user.username} - Appearance Preferences"
  