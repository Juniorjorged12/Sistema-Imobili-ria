from django.contrib import admin
from .models import Bairro


@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade')
    list_filter = ('cidade',)
    search_fields = ('nome',)
