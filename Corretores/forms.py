from .models import Corretor
from django import forms

class CorretorForm(forms.ModelForm):
    class Meta:
        model = Corretor
        fields = '__all__'