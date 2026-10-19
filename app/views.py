from django.shortcuts import render

from Bairros.models import Bairro
from Cidades.models import Cidade
from Corretores.models import Corretor
from Imoveis.models import Imovel


def home(request):
    context = {
        "total_imoveis": Imovel.objects.count(),
        "total_cidades": Cidade.objects.count(),
        "total_bairros": Bairro.objects.count(),
        "total_corretores": Corretor.objects.count(),
        "imoveis": Imovel.objects.filter(status="disponivel")
        .select_related("cidade", "bairro")
        .prefetch_related("fotos")
        .order_by("-pk")[:6],
    }
    return render(request, "home.html", context)