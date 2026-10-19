import io
import tempfile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils.datastructures import MultiValueDict
from django.urls import reverse
from PIL import Image

from Bairros.models import Bairro
from Cidades.models import Cidade
from Corretores.models import Corretor
from Imoveis.models import Imovel
from .forms import FotoImovelUploadForm
from .models import Fotoimovel


class FotoImovelGalleryTests(TestCase):
    def setUp(self):
        temporary_media = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_media.cleanup)
        media_settings = override_settings(MEDIA_ROOT=temporary_media.name)
        media_settings.enable()
        self.addCleanup(media_settings.disable)

        self.cidade = Cidade.objects.create(nome="Cidade de teste")
        self.bairro = Bairro.objects.create(nome="Bairro de teste", cidade=self.cidade)
        usuario = User.objects.create_user(username="corretor-teste")
        corretor = Corretor.objects.create(usuario=usuario)
        self.imovel = Imovel.objects.create(
            finalidade="venda",
            tipo="casa",
            cidade=self.cidade,
            bairro=self.bairro,
            endereco="Rua de teste, 10",
            valor="250000.00",
            dormitorios=2,
            suites=1,
            banheiros=2,
            vagas=1,
            area_total="100.00",
            area_construida="80.00",
            descricao="",
            status="disponivel",
            corretor=corretor,
            piscina=False,
        )

    def _imagem(self, nome):
        conteudo = io.BytesIO()
        Image.new("RGB", (2, 2), color="white").save(conteudo, format="PNG")
        return SimpleUploadedFile(nome, conteudo.getvalue(), content_type="image/png")

    def _criar_fotos(self, quantidade):
        for indice in range(quantidade):
            Fotoimovel.objects.create(
                imovel=self.imovel,
                imagem=self._imagem(f"foto-{indice}.png"),
            )

    def test_permite_no_maximo_doze_fotos_por_imovel(self):
        self._criar_fotos(Fotoimovel.MAX_FOTOS_POR_IMOVEL)

        with self.assertRaises(ValidationError):
            Fotoimovel.objects.create(
                imovel=self.imovel,
                imagem=self._imagem("foto-extra.png"),
            )

    def test_formulario_aceita_multiplos_arquivos_dentro_do_limite(self):
        self._criar_fotos(10)
        form = FotoImovelUploadForm(
            data={"imovel": str(self.imovel.pk)},
            files=MultiValueDict(
                {"imagens": [self._imagem("foto-10.png"), self._imagem("foto-11.png")]}
            ),
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(len(form.cleaned_data["imagens"]), 2)

    def test_formulario_rejeita_upload_que_ultrapassa_limite_do_imovel(self):
        self._criar_fotos(11)
        form = FotoImovelUploadForm(
            data={"imovel": str(self.imovel.pk)},
            files=MultiValueDict(
                {"imagens": [self._imagem("foto-11.png"), self._imagem("foto-12.png")]}
            ),
        )

        self.assertFalse(form.is_valid())
        self.assertIn("imagens", form.errors)

    def test_view_salva_varias_fotos_no_mesmo_envio(self):
        response = self.client.post(
            reverse("fotos_create"),
            {
                "imovel": str(self.imovel.pk),
                "imagens": [self._imagem("lote-1.png"), self._imagem("lote-2.png")],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.imovel.fotos.count(), 2)

    def test_detalhe_do_imovel_exibe_todas_as_fotos(self):
        self._criar_fotos(3)

        response = self.client.get(
            reverse("imoveis_detail", kwargs={"pk": self.imovel.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"].fotos.count(), 3)
        for foto in self.imovel.fotos.all():
            self.assertContains(response, foto.imagem.url)
