
# Create your models here.
from django.db import models
from Categories.models import Produit

class promo(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='promos')  # علاقة مع Produit

    def __str__(self):
        # الوصول مباشرة لبيانات المنتج
        return f"{self.produit.nom} - {self.produit.prix} - {self.produit.photo} - {self.produit.description}"
