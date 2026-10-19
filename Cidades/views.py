from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from .serializers import CidadeSerializer
from .models import Cidade
from rest_framework import generics
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import CidadeForm


class CidadeWebContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "list_url": "cidades_list",
            "create_url": "cidades_create",
            "detail_url": "cidades_detail",
            "update_url": "cidades_update",
            "delete_url": "cidades_delete",
        })
        return context


class CidadeFormStyleMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"
        return form


class CidadeListView(CidadeWebContextMixin, ListView):
    model = Cidade
    template_name = 'cidades_list.html'
    context_object_name = 'cidades'

    def get_queryset(self):
        return Cidade.objects.order_by("nome")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rows"] = [
            {"object": cidade, "values": [cidade.pk, cidade.nome]}
            for cidade in context["cidades"]
        ]
        context["column_labels"] = ["Código", "Nome"]
        return context


class CidadeDetailView(CidadeWebContextMixin, DetailView):
    model = Cidade
    template_name = "cidades_detail.html"


class CidadeCreateView(CidadeWebContextMixin, CidadeFormStyleMixin, CreateView):
    model = Cidade
    form_class = CidadeForm
    template_name = 'cidades_create.html'
    success_url = reverse_lazy('cidades_list')

    def get_success_url(self):
        messages.success(self.request, "Cidade cadastrada com sucesso.")
        return super().get_success_url()


class CidadeUpdateView(CidadeWebContextMixin, CidadeFormStyleMixin, UpdateView):
    model = Cidade
    form_class = CidadeForm
    template_name = 'cidades_update.html'
    success_url = reverse_lazy('cidades_list')

    def get_success_url(self):
        messages.success(self.request, "Cidade atualizada com sucesso.")
        return super().get_success_url()


class CidadeDeleteView(CidadeWebContextMixin, DeleteView):
    model = Cidade
    template_name = 'cidades_delete.html'
    success_url = reverse_lazy('cidades_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, "Esta cidade está vinculada a imóveis e não pode ser excluída.")
            return redirect(self.success_url)
        messages.success(self.request, "Cidade excluída com sucesso.")
        return response




class CidadeListCreateView(generics.ListCreateAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer


class CidadeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
