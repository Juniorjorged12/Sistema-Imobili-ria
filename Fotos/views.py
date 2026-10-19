from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Fotoimovel
from .forms import FotoImovelForm, FotoImovelUploadForm


class FotoimovelWebContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "list_url": "fotos_list",
            "create_url": "fotos_create",
            "detail_url": "fotos_detail",
            "update_url": "fotos_update",
            "delete_url": "fotos_delete",
        })
        return context


class FotoimovelFormStyleMixin:
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


class FotoimovelListView(FotoimovelWebContextMixin, ListView):
    model = Fotoimovel
    template_name = 'fotos_list.html'
    context_object_name = 'fotos'

    def get_queryset(self):
        return Fotoimovel.objects.select_related("imovel").order_by("-pk")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rows"] = [{"object": foto, "values": [foto.pk]} for foto in context["fotos"]]
        context["column_labels"] = ["Código"]
        return context


class FotoimovelDetailView(FotoimovelWebContextMixin, DetailView):
    model = Fotoimovel
    template_name = "fotos_detail.html"

    def get_queryset(self):
        return Fotoimovel.objects.select_related("imovel")


class FotoimovelCreateView(FotoimovelWebContextMixin, FotoimovelFormStyleMixin, CreateView):
    model = Fotoimovel
    form_class = FotoImovelUploadForm
    template_name = 'fotos_create.html'
    success_url = reverse_lazy('fotos_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("instance", None)
        return kwargs

    def form_valid(self, form):
        imovel = form.cleaned_data["imovel"]
        imagens = form.cleaned_data["imagens"]
        with transaction.atomic():
            imovel = imovel.__class__.objects.select_for_update().get(pk=imovel.pk)
            if imovel.fotos.count() + len(imagens) > Fotoimovel.MAX_FOTOS_POR_IMOVEL:
                form.add_error(
                    "imagens",
                    "O limite de 12 fotos por imóvel foi atingido durante o envio.",
                )
                return self.form_invalid(form)
            for imagem in imagens:
                Fotoimovel.objects.create(imovel=imovel, imagem=imagem)
        messages.success(self.request, f"{len(imagens)} foto(s) adicionada(s) com sucesso.")
        return redirect(self.success_url)


class FotoimovelUpdateView(FotoimovelWebContextMixin, FotoimovelFormStyleMixin, UpdateView):
    model = Fotoimovel
    form_class = FotoImovelForm
    template_name = 'fotos_update.html'
    success_url = reverse_lazy('fotos_list')

    def get_success_url(self):
        messages.success(self.request, "Foto atualizada com sucesso.")
        return super().get_success_url()


class FotoimovelDeleteView(FotoimovelWebContextMixin, DeleteView):
    model = Fotoimovel
    template_name = 'fotos_delete.html'
    success_url = reverse_lazy('fotos_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Foto excluída com sucesso.")
        return response
