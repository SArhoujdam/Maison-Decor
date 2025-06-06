import os
import django

# تهيئة إعدادات دجانجو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PFE.settings')
django.setup()

from PFE.models import Commande  # استخدم اسم تطبيقك الحقيقي هنا

def debug_data():
    print("="*50)
    print("تقرير تصحيح الأخطاء")
    print(f"عدد الطلبات: {Commande.objects.count()}")
    
    if Commande.objects.exists():
        print("عينة من الطلبات:")
        for cmd in Commande.objects.all()[:3]:
            print(f"- ID: {cmd.id}")
            print(f"  المستخدم: {cmd.user.username}")
            print(f"  العنوان: {cmd.adresse_livraison}")
            print(f"  التاريخ: {cmd.date_commande}")
            print(f"  المنتجات: {[p.nom for p in cmd.produits.all()]}")
    else:
        print("لا توجد طلبات في قاعدة البيانات")
    
    print("="*50)

if __name__ == "__main__":
    debug_data()