from django.contrib import admin
from .models import Cidade


@admin.register(Cidade)
class CidadesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    
