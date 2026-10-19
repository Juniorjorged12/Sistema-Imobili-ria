from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from .serializers import BairroSerializer
from .models import Bairro
from rest_framework import generics
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import BairroForm


class BairroWebContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "list_url": "bairros_list",
            "create_url": "bairros_create",
            "detail_url": "bairros_detail",
            "update_url": "bairros_update",
            "delete_url": "bairros_delete",
        })
        return context


class BairroFormStyleMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            input_type = getattr(field.widget, "input_type", None)
            field.widget.attrs["class"] = "form-select" if input_type == "select" else "form-control"
        return form


class BairroListView(BairroWebContextMixin, ListView):
    model = Bairro
    template_name = 'bairros_list.html'
    context_object_name = 'bairros'

    def get_queryset(self):
        return Bairro.objects.select_related("cidade").order_by("nome")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rows"] = [
            {"object": bairro, "values": [bairro.pk, bairro.nome, bairro.cidade]}
            for bairro in context["bairros"]
        ]
        context["column_labels"] = ["Código", "Nome", "Cidade"]
        return context


class BairroDetailView(BairroWebContextMixin, DetailView):
    model = Bairro
    template_name = "bairros_detail.html"

    def get_queryset(self):
        return Bairro.objects.select_related("cidade")


class BairroCreateView(BairroWebContextMixin, BairroFormStyleMixin, CreateView):
    model = Bairro
    form_class = BairroForm
    template_name = 'bairros_create.html'
    success_url = reverse_lazy('bairros_list')

    def get_success_url(self):
        messages.success(self.request, "Bairro cadastrado com sucesso.")
        return super().get_success_url()


class BairroUpdateView(BairroWebContextMixin, BairroFormStyleMixin, UpdateView):
    model = Bairro
    form_class = BairroForm
    template_name = 'bairros_update.html'
    success_url = reverse_lazy('bairros_list')

    def get_success_url(self):
        messages.success(self.request, "Bairro atualizado com sucesso.")
        return super().get_success_url()


class BairroDeleteView(BairroWebContextMixin, DeleteView):
    model = Bairro
    template_name = 'bairros_delete.html'
    success_url = reverse_lazy('bairros_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, "Este bairro está vinculado a imóveis e não pode ser excluído.")
            return redirect(self.success_url)
        messages.success(self.request, "Bairro excluído com sucesso.")
        return response




class BairroListCreateView(generics.ListCreateAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroSerializer


class BairroRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroSerializer
