from .models import Fotoimovel
from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        clean_one = super().clean
        if isinstance(data, (list, tuple)):
            return [clean_one(item, initial) for item in data]
        if data:
            return [clean_one(data, initial)]
        return []


class FotoImovelForm(forms.ModelForm):
    class Meta:
        model = Fotoimovel
        fields = '__all__'


class FotoImovelUploadForm(forms.Form):
    imovel = forms.ModelChoiceField(
        queryset=None,
        label="Imóvel",
        empty_label="Selecione um imóvel",
    )
    imagens = MultipleFileField(
        label="Imagens",
        help_text="Selecione até 12 imagens. Você pode selecionar várias de uma vez.",
    )

    def __init__(self, *args, **kwargs):
        from Imoveis.models import Imovel

        super().__init__(*args, **kwargs)
        self.fields["imovel"].queryset = Imovel.objects.order_by("pk")
        self.fields["imagens"].widget.attrs.update({
            "class": "visually-hidden file-picker-input",
            "aria-describedby": "imagens-selecionadas",
        })

    def clean_imagens(self):
        imagens = self.cleaned_data["imagens"]
        if not imagens:
            raise forms.ValidationError("Selecione pelo menos uma imagem.")
        if len(imagens) > Fotoimovel.MAX_FOTOS_POR_IMOVEL:
            raise forms.ValidationError("Você pode enviar no máximo 12 imagens por vez.")
        return imagens

    def clean(self):
        cleaned_data = super().clean()
        imovel = cleaned_data.get("imovel")
        imagens = cleaned_data.get("imagens")
        if imovel and imagens:
            quantidade_atual = imovel.fotos.count()
            if quantidade_atual + len(imagens) > Fotoimovel.MAX_FOTOS_POR_IMOVEL:
                disponiveis = Fotoimovel.MAX_FOTOS_POR_IMOVEL - quantidade_atual
                self.add_error(
                    "imagens",
                    f"Este imóvel tem {quantidade_atual} foto(s). "
                    f"Você ainda pode adicionar {max(disponiveis, 0)}.",
                )
        return cleaned_data