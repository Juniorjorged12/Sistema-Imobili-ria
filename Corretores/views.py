from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from .serializers import CorretorSerializer
from .models import Corretor
from rest_framework import generics
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import CorretorForm


class CorretorWebContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "list_url": "corretores_list",
            "create_url": "corretores_create",
            "detail_url": "corretores_detail",
            "update_url": "corretores_update",
            "delete_url": "corretores_delete",
        })
        return context


class CorretorFormStyleMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            input_type = getattr(field.widget, "input_type", None)
            field.widget.attrs["class"] = "form-select" if input_type == "select" else "form-control"
        return form


class CorretorListView(CorretorWebContextMixin, ListView):
    model = Corretor
    template_name = 'corretores_list.html'
    context_object_name = 'corretores'

    def get_queryset(self):
        return Corretor.objects.select_related("usuario").order_by("usuario__username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rows"] = [
            {
                "object": corretor,
                "values": [corretor.pk, corretor.usuario, corretor.creci, corretor.telefone],
            }
            for corretor in context["corretores"]
        ]
        context["column_labels"] = ["Código", "Usuário", "CRECI", "Telefone"]
        return context


class CorretorDetailView(CorretorWebContextMixin, DetailView):
    model = Corretor
    template_name = "corretores_detail.html"

    def get_queryset(self):
        return Corretor.objects.select_related("usuario")


class CorretorCreateView(CorretorWebContextMixin, CorretorFormStyleMixin, CreateView):
    model = Corretor
    form_class = CorretorForm
    template_name = 'corretores_create.html'
    success_url = reverse_lazy('corretores_list')

    def get_success_url(self):
        messages.success(self.request, "Corretor cadastrado com sucesso.")
        return super().get_success_url()


class CorretorUpdateView(CorretorWebContextMixin, CorretorFormStyleMixin, UpdateView):
    model = Corretor
    form_class = CorretorForm
    template_name = 'corretores_update.html'
    success_url = reverse_lazy('corretores_list')

    def get_success_url(self):
        messages.success(self.request, "Corretor atualizado com sucesso.")
        return super().get_success_url()


class CorretorDeleteView(CorretorWebContextMixin, DeleteView):
    model = Corretor
    template_name = 'corretores_delete.html'
    success_url = reverse_lazy('corretores_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, "Este corretor está vinculado a imóveis e não pode ser excluído.")
            return redirect(self.success_url)
        messages.success(self.request, "Corretor excluído com sucesso.")
        return response



class CorretorListCreateView(generics.ListCreateAPIView):
    queryset = Corretor.objects.all()
    serializer_class = CorretorSerializer


class CorretorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Corretor.objects.all()
    serializer_class = CorretorSerializer

