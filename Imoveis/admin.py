from django.contrib import admin
from .models import Imovel
from Fotos.models import Fotoimovel


class FotoImovelInline(admin.TabularInline):
    model = Fotoimovel
    extra = 3
    fields = ('imagem', 'destaque')
    can_delete = True


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('id','tipo', 'finalidade', 'cidade', 'bairro', 'valor', 'status','endereco','corretor','piscina')
    list_filter = ('finalidade', 'tipo', 'cidade', 'bairro', 'status')
    search_fields = ('cidade__nome', 'bairro__nome', 'descricao')
    ordering = ('-valor',)
    inlines = [FotoImovelInline]
