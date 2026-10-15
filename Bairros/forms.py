from .models import Bairro
from django import forms


class BairroForm(forms.ModelForm):
    class Meta:
        model = Bairro
        fields = '__all__'