from .models import Imovel
from django import forms
from Bairros.models import Bairro
from Cidades.models import Cidade


class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        city_id = (
            self.data.get(self.add_prefix("cidade"))
            if self.is_bound
            else self.instance.cidade_id
        )
        if city_id:
            self.fields["bairro"].queryset = Bairro.objects.filter(
                cidade_id=city_id
            ).order_by("nome")
        else:
            self.fields["bairro"].queryset = Bairro.objects.none()


class ImovelSearchForm(forms.Form):
    finalidade = forms.ChoiceField(
        label="Finalidade",
        choices=[("", "Todas")] + Imovel.FINALIDADE_CHOICES,
        required=False,
    )
    tipo = forms.ChoiceField(
        label="Tipo",
        choices=[("", "Todos")] + Imovel.TIPO_CHOICES,
        required=False,
    )
    cidade = forms.ModelChoiceField(
        label="Cidade",
        queryset=Cidade.objects.none(),
        empty_label="Todas",
        required=False,
    )
    bairro = forms.ModelChoiceField(
        label="Bairro",
        queryset=Bairro.objects.none(),
        empty_label="Todos",
        required=False,
    )
    ordenacao = forms.ChoiceField(
        label="Ordenar por valor",
        choices=[
            ("", "Mais recentes"),
            ("valor_asc", "Menor valor"),
            ("valor_desc", "Maior valor"),
        ],
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cidade"].queryset = Cidade.objects.order_by("nome")
        self.fields["bairro"].queryset = Bairro.objects.select_related("cidade").order_by(
            "cidade__nome", "nome"
        )
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select"