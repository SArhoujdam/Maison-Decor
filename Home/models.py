from django.db import models
from Categories.models import Produit

class Home(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='homes') 
    # علاقة مع Produit

    def __str__(self):
    
        return f"{self.produit.nom} - {self.produit.prix} - {self.produit.photo} - {self.produit.description}"
