from .models import Fotoimovel
from django import forms


class FotoImovelForm(forms.ModelForm):
    class Meta:
        model = Fotoimovel
        fields = '__all__'