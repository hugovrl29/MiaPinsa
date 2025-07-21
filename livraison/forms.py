from django import forms
from .models import *


class CommandForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            'produit_libelle'
        ]
