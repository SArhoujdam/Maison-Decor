import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PFE.settings')
django.setup()

from PFE.models import Commande  

def debug_data():
    print("="*50)
    print(" commande Debug Information")
    print(f" number of commandes: {Commande.objects.count()}")
    
    if Commande.objects.exists():
        print("information for the first 3 commandes:")
        for cmd in Commande.objects.all()[:3]:
            print(f"- ID: {cmd.id}")
            print(f"  user: {cmd.user.username}")
            print(f"  Address: {cmd.adresse_livraison}")
            print(f"  Quantity: {cmd.quantite}")
            print(f"  Date: {cmd.date_commande}")
            print(f"  Products: {[p.nom for p in cmd.produits.all()]}")
    else:
        print("No commandes found.")
    
    print("="*50)

if __name__ == "__main__":
    debug_data()
