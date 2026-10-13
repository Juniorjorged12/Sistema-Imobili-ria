from django.contrib import admin
from .models import Corretor


@admin.register(Corretor)
class CorretorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creci', 'telefone')
    search_fields = ('usuario', 'creci')