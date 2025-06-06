from django import forms
from .models import Categorie

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
