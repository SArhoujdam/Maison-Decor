from django.urls import path
from . import views

urlpatterns = [

  path('contact/', views.contact1, name='contact1'),
]