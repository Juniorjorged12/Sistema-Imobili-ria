from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .serializers import ImovelSerializer
from .models import Imovel
from Bairros.models import Bairro
from rest_framework import generics
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import ImovelForm, ImovelSearchForm


@login_required
def bairros_por_cidade(request):
    city_id = request.GET.get("cidade")
    if not city_id or not city_id.isdecimal():
        return JsonResponse({"error": "Selecione uma cidade válida."}, status=400)

    bairros = Bairro.objects.filter(cidade_id=city_id).order_by("nome")
    return JsonResponse(
        [{"id": bairro.pk, "nome": bairro.nome} for bairro in bairros],
        safe=False,
    )


class ImovelWebContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "list_url": "imoveis_list",
            "create_url": "imoveis_create",
            "detail_url": "imoveis_detail",
            "update_url": "imoveis_update",
            "delete_url": "imoveis_delete",
        })
        return context


class ImovelFormStyleMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            input_type = getattr(field.widget, "input_type", None)
            if input_type == "checkbox":
                field.widget.attrs["class"] = "form-check-input"
            elif input_type == "select":
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"
        return form


class ImovelListView(ListView):
    model = Imovel
    template_name = 'imoveis_list.html'
    context_object_name = 'imoveis'

    def get_search_form(self):
        if not hasattr(self, "search_form"):
            self.search_form = ImovelSearchForm(self.request.GET)
        return self.search_form

    def get_queryset(self):
        queryset = (
            Imovel.objects.select_related("cidade", "bairro")
            .prefetch_related("fotos")
            .order_by("-pk")
        )
        form = self.get_search_form()
        if not form.is_valid():
            return queryset

        filters = form.cleaned_data
        if filters["finalidade"]:
            queryset = queryset.filter(finalidade=filters["finalidade"])
        if filters["tipo"]:
            queryset = queryset.filter(tipo=filters["tipo"])
        if filters["cidade"]:
            queryset = queryset.filter(cidade=filters["cidade"])
        if filters["bairro"]:
            queryset = queryset.filter(bairro=filters["bairro"])

        ordering = {
            "valor_asc": "valor",
            "valor_desc": "-valor",
        }.get(filters["ordenacao"], "-pk")
        return queryset.order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "search_form": self.get_search_form(),
            "list_url": "imoveis_list",
            "create_url": "imoveis_create",
            "detail_url": "imoveis_detail",
            "column_labels": ["Código", "Finalidade", "Tipo", "Cidade", "Bairro", "Valor", "Status"],
            "rows": [
                {
                    "object": imovel,
                    "values": [
                        imovel.pk,
                        imovel.get_finalidade_display(),
                        imovel.get_tipo_display(),
                        imovel.cidade,
                        imovel.bairro,
                        imovel.valor,
                        imovel.get_status_display(),
                    ],
                }
                for imovel in context["imoveis"]
            ],
        })
        return context


class ImovelDetailView(ImovelWebContextMixin, DetailView):
    model = Imovel
    template_name = "imoveis_detail.html"
    context_object_name = "object"

    def get_queryset(self):
        return Imovel.objects.select_related("cidade", "bairro", "corretor").prefetch_related("fotos")


class ImovelCreateView(ImovelWebContextMixin, ImovelFormStyleMixin, CreateView):
    model = Imovel
    form_class = ImovelForm
    template_name = 'imoveis_create.html'
    success_url = reverse_lazy('imoveis_list')


class ImovelUpdateView(ImovelWebContextMixin, ImovelFormStyleMixin, UpdateView):
    model = Imovel
    form_class = ImovelForm
    template_name = 'imoveis_update.html'
    success_url = reverse_lazy('imoveis_list')


class ImovelDeleteView(ImovelWebContextMixin, DeleteView):
    model = Imovel
    template_name = 'imoveis_delete.html'
    success_url = reverse_lazy('imoveis_list')

    def form_valid(self, form):
        messages.success(self.request, "Imóvel excluído com sucesso.")
        return super().form_valid(form)




class ImovelListCreateView(generics.ListCreateAPIView):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer


class ImovelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer
