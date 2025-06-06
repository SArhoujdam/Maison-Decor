
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='categories/')
    slug = models.SlugField(unique=True, blank=True, null=True)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='produits/')
    quantite = models.IntegerField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


