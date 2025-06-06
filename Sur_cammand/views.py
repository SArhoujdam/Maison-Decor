from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from Categories.models import Categorie

# استيراد النماذج المطلوبة
from profileapp.models import Profileapp  # عدّل المسار حسب تطبيقك الحقيقي
      # عدّل المسار حسب تطبيقك الحقيقي

def Sur_cammand_View(request):
    categories = Categorie.objects.all()

    # جلب profile و products حسب حالة تسجيل الدخول
    if request.user.is_authenticated:
        try:
            profile = Profileapp.objects.get(user=request.user)
        except Profileapp.DoesNotExist:
            profile = None
        
    else:
        profile = None
        

    if request.method == 'POST':
        name = request.POST.get('user_name')
        email = request.POST.get('user_email')
        menu_option = request.POST.get('menu_option')
        length = request.POST.get('length')
        height = request.POST.get('height')
        color = request.POST.get('color')
        message = request.POST.get('message')
        image = request.FILES.get('image_model')

        full_message = (
            f"Nom: {name}\n"
            f"Email: {email}\n"
            f"Produit: {menu_option}\n"
            f"Dimensions: {length} cm x {height} cm\n"
            f"Couleur: {color}\n"
            f"Message:\n{message or '---'}"
        )

        try:
            email_message = EmailMessage(
                subject=f"Nouvelle commande personnalisée - {menu_option}",
                body=full_message,
                from_email=settings.EMAIL_HOST_USER,
                to=['sarhoujdam@gmail.com'],
                reply_to=[email],
            )

            if image:
                email_message.attach(image.name, image.read(), image.content_type)

            email_message.send(fail_silently=False)

            messages.success(request, "✅ Votre commande a été envoyée avec succès !")
            return render(request, 'sur_command/Sur_cammand.html', {
                'success': True,
                'categories': categories,
                'profile': profile,
                
            })
        except Exception as e:
            messages.error(request, f"❌ Une erreur s'est produite : {str(e)}")
            return render(request, 'sur_command/Sur_cammand.html', {
                'error': str(e),
                'categories': categories,
                'profile': profile,
                
            })

    return render(request, 'sur_command/Sur_cammand.html', {
        'categories': categories,
        'profile': profile,
        
    })
