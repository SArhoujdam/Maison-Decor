from django.contrib import admin
from .models import Commande, UserAppearancePreferences  # استيراد الموديل من نفس التطبيق

admin.site.register(Commande)
admin.site.register(UserAppearancePreferences)