from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.Sur_cammand_View, name='Sur_cammand'), 
] 