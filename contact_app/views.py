from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from profileapp.models import Profileapp   # تأكد من اسم التطبيق والمسار الصحيح
      # تأكد من اسم التطبيق والمسار الصحيح

def contact1(request):
    # شرط المستخدم
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
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"Email: {email}\nSubject: {subject}\nNom: {name}\nMessage:\n{message}"

        try:
            email_message = EmailMessage(
                subject=subject,
                body=full_message,
                from_email=settings.EMAIL_HOST_USER,
                to=['sarhoujdam@gmail.com'],
                reply_to=[email],
            )
            email_message.send(fail_silently=False)

            messages.success(request, "✅ Votre message a été envoyé avec succès !")
            return render(request, 'contact_app/contact.html', {
                'success': True,
                'profile': profile,
                
            })
        except Exception as e:
            messages.error(request, f"❌ Une erreur s'est produite : {str(e)}")
            return render(request, 'contact_app/contact.html', {
                'error': str(e),
                'profile': profile,
               
            })

    return render(request, 'contact_app/contact.html', {
        'profile': profile,
        
    })











