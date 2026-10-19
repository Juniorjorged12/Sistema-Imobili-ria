from django.db import models
from django.core.exceptions import ValidationError

class Fotoimovel(models.Model):
    MAX_FOTOS_POR_IMOVEL = 12

    imovel = models.ForeignKey('Imoveis.Imovel', on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='fotos/')
    destaque = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.imovel_id:
            fotos_existentes = Fotoimovel.objects.filter(imovel_id=self.imovel_id)
            if self.pk:
                fotos_existentes = fotos_existentes.exclude(pk=self.pk)
            if fotos_existentes.count() >= self.MAX_FOTOS_POR_IMOVEL:
                raise ValidationError({
                    "imovel": "Este imóvel já possui o limite máximo de 12 fotos."
                })

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Foto de {self.imovel}"
