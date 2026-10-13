from django.contrib import admin
from .models import Fotoimovel


@admin.register(Fotoimovel)
class FotoimovelAdmin(admin.ModelAdmin):
    list_display = ('id', 'imovel', 'destaque')
    search_fields = ('imovel_id', 'imovel__tipo', 'imovel__bairro__nome', 'imovel__cidade__nome')
    list_filter = ('destaque', 'imovel')


